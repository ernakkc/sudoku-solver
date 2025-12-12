from pysat.solvers import Glucose3

class SudokuSAT:
    def __init__(self):
        # Glucose3, popüler ve hızlı bir SAT çözücüdür.
        self.solver = Glucose3()

    def _to_var(self, row, col, val):
        """
        Slayttaki p(i, j, n) önermesini tek bir sayıya (ID) çevirir.
        Row: 0-8, Col: 0-8, Val: 1-9
        """
        return (row * 81) + (col * 9) + (val - 1) + 1

    def _to_grid(self, var_id):
        """
        Değişken ID'sini tekrar (row, col, val) formatına çevirir.
        """
        adjusted = var_id - 1
        val = (adjusted % 9) + 1
        col = (adjusted // 9) % 9
        row = adjusted // 81
        return row, col, val

    def add_constraints(self):
        """
        Slaytlardaki matematiksel kuralları (Encoding) burada ekliyoruz.
        """
        
        # 1. KURAL: Her hücrede en az bir sayı olmalıdır.
        # Slayt notu: V (p(i,j,1) v p(i,j,2) ... v p(i,j,9))
        for r in range(9):
            for c in range(9):
                self.solver.add_clause([self._to_var(r, c, v) for v in range(1, 10)])

        # 2. KURAL: Her hücrede en fazla bir sayı olabilir.
        # Slayt notu: p(i,j,n) -> -p(i,j,n') (Eğer n varsa, n' olamaz)
        for r in range(9):
            for c in range(9):
                for v1 in range(1, 10):
                    for v2 in range(v1 + 1, 10):
                        # (-v1 V -v2) şeklinde eklenir (De Morgan kuralı gereği)
                        self.solver.add_clause([-self._to_var(r, c, v1), -self._to_var(r, c, v2)])

        # 3. KURAL: Her satırda her sayıdan tam olarak bir tane olmalı.
        # Slayt 63'teki formül.
        for r in range(9):
            for v in range(1, 10):
                self.solver.add_clause([self._to_var(r, c, v) for c in range(9)])

        # 4. KURAL: Her sütunda her sayıdan tam olarak bir tane olmalı.
        # Slayt 64'teki formül.
        for c in range(9):
            for v in range(1, 10):
                self.solver.add_clause([self._to_var(r, c, v) for r in range(9)])

        # 5. KURAL: Her 3x3 blokta her sayıdan tam olarak bir tane olmalı.
        # Slayt 65'teki formül.
        for br in range(3): # Blok satırı (0,1,2)
            for bc in range(3): # Blok sütunu (0,1,2)
                for v in range(1, 10):
                    clause = []
                    for i in range(3):
                        for j in range(3):
                            r = br * 3 + i
                            c = bc * 3 + j
                            clause.append(self._to_var(r, c, v))
                    self.solver.add_clause(clause)

    def is_solvable(self, input_grid):
        """
        Verilen Sudoku puzzle'ının çözülebilir olup olmadığını kontrol eder.
        
        Args:
            input_grid: 9x9 puzzle (0=boş hücre)
        
        Returns:
            tuple: (solvable: bool, error_msg: str or None)
        """
        # Temel kuralları ekle
        self.add_constraints()

        # Verilen sayıları kısıtlama olarak ekle
        for r in range(9):
            for c in range(9):
                val = input_grid[r][c]
                if val != 0:
                    if val < 1 or val > 9:
                        return False, f"Invalid value: {val} at ({r}, {c})"
                    self.solver.add_clause([self._to_var(r, c, val)])

        # Test the SAT solver
        if self.solver.solve():
            return True, None
        else:
            return False, "This Sudoku puzzle has no solution."

    def solve_sudoku(self, input_grid):
        """
        Takes a 9x9 matrix from the API, solves it, and returns the result.
        Zeros are considered empty cells.
        """
        # Temel kuralları ekle
        self.add_constraints()

        # 6. KURAL: Verilen ipuçlarını (OCR'dan gelen sayıları) kısıtlama olarak ekle.
        for r in range(9):
            for c in range(9):
                val = input_grid[r][c]
                if val != 0:
                    # Bu hücre kesinlikle bu değerdir.
                    self.solver.add_clause([self._to_var(r, c, val)])

        # Çözümleme işlemi
        if self.solver.solve():
            model = self.solver.get_model()
            result_grid = [[0 for _ in range(9)] for _ in range(9)]
            
            # Modelden dönen "True" değişkenleri grid'e işle
            for var in model:
                if var > 0: # Sadece pozitif (seçilmiş) değişkenleri al
                    r, c, v = self._to_grid(var)
                    result_grid[r][c] = v
            return result_grid
        else:
            print("Çözüm bulunamadı")
            return None # Çözüm yok

# --- ÖRNEK KULLANIM (Main Blok) ---
if __name__ == "__main__":
    # Örnek: 0'lar boş hücreleri temsil eder.
    # API'den aldığın 9x9 matris bu formatta olacak.
    sample_puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    solver_app = SudokuSAT()
    solution = solver_app.solve_sudoku(sample_puzzle)

    if solution:
        print("Çözüm Bulundu:")
        for row in solution:
            print(row)
    else:
        print("Çözüm Yok!")