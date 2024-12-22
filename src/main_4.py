import tkinter as tk
from tkinter import ttk
import db

# ### 텀1, 텀2 는 시간이 같아도 중복 추가하기 가능하게 구현하기

class MainGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("예술공학부 시간표 시뮬레이션")
        
        # 시간표 데이터
        self.time_slots = ["9:30 - 10:30", "10:30 - 11:30", "11:30 - 12:30", "12:30 - 13:30", "13:30 - 14:30", "14:30 - 15:30", "15:30 - 16:30", "16:30 - 17:30", "17:30 - 18:30"]
        self.days = ["월", "화", "수", "목", "금"]
        self.day_map = {"월": 0, "화": 1, "수": 2, "목": 3, "금": 4}
        self.timetable_cells_term_1 = {}  # 시간표 셀을 저장할 딕셔너리
        self.timetable_cells_term_2 = {}  # 시간표 셀을 저장할 딕셔너리
        self.cell_subject_map_term_1 = {}  # 시간표 셀과 과목 정보를 매핑할 딕셔너리
        self.cell_subject_map_term_2 = {}  # 시간표 셀과 과목 정보를 매핑할 딕셔너리
        
        self.create_main_frame()
        self.create_left_frame()
        self.create_right_frame()
        self.create_bottom_left_frame()
        self.create_bottom_right_frame()
        self.create_current_credits()
    def create_main_frame(self):
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 좌우 프레임을 1:1 비율로 설정
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)

    def create_left_frame(self):
        # 왼쪽 프레임 (시간표 term1)
        self.left_frame = ttk.LabelFrame(self.main_frame, text="Term 1", padding="5")
        self.left_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        self.create_timetable_term_1()

    def create_right_frame(self):
        # 오른쪽 프레임 (시간표 term2)
        self.right_frame = ttk.LabelFrame(self.main_frame, text="Term 2", padding="5")
        self.right_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        self.create_timetable_term_2()

    def create_bottom_left_frame(self):
        # 하단 프레임
        self.bottom_left_frame = ttk.LabelFrame(self.main_frame, text="추가된 강의", padding="5")
        self.bottom_left_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.create_bottom_left_content()

    def create_bottom_right_frame(self):
        # 하단 프레임
        self.bottom_right_frame = ttk.LabelFrame(self.main_frame, text="전체 강의 목록", padding="5")
        self.bottom_right_frame.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        
        self.create_bottom_right_content()

    def create_bottom_left_content(self):
        # LabelFrame으로 변경하여 제목 표시
        self.bottom_left_frame = ttk.LabelFrame(self.main_frame, text="추가된 강의 [항목을 더블클릭하면 삭제 됩니다!]", padding="5")
        self.bottom_left_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        # 트리뷰 생성
        columns = ('대학', '개설학과', '이수구분', '과목명', '과목번호', '학점', '담당교수', '강의시간1', '강의시간2', '강의실', '텀')
        self.added_subjects_tree = ttk.Treeview(self.bottom_left_frame, columns=columns, show="headings")
        
        # 컬럼 설정
        for col in columns:
            self.added_subjects_tree.heading(col, text=col)
            self.added_subjects_tree.column(col, width=70)
        
        # 스크롤바 추가
        scrollbar = ttk.Scrollbar(self.bottom_left_frame, orient="vertical", command=self.added_subjects_tree.yview)
        self.added_subjects_tree.configure(yscrollcommand=scrollbar.set)
        
        # 배치
        self.added_subjects_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 버튼 프레임 추가
        button_frame = ttk.Frame(self.bottom_left_frame)
        button_frame.pack(side="bottom", fill="x", pady=5)

        # 더블클릭 이벤트 바인딩
        self.added_subjects_tree.bind("<Double-1>", lambda e: self.remove_from_left())

    def create_bottom_right_content(self):
        # LabelFrame으로 변경하여 제목 표시
        self.bottom_right_frame = ttk.LabelFrame(self.main_frame, text="강의 목록 [항목을 더블클릭하면 추가 됩니다!]", padding="5")
        self.bottom_right_frame.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        # 트리뷰 생성
        columns = ('대학', '개설학과', '이수구분', '과목명', '과목번호', '학점', '담당교수', '강의시간1', '강의시간2', '강의실', '텀')
        self.full_subjects_tree = ttk.Treeview(self.bottom_right_frame, columns=columns, show="headings")
        
        # 컬럼 설정
        for col in columns:
            self.full_subjects_tree.heading(col, text=col)
            self.full_subjects_tree.column(col, width=70)
        
        for subject in db.GetSubjects():
            self.full_subjects_tree.insert("", "end", values=subject)
        # 스크롤바 추가
        scrollbar = ttk.Scrollbar(self.bottom_right_frame, orient="vertical", command=self.full_subjects_tree.yview)
        self.full_subjects_tree.configure(yscrollcommand=scrollbar.set)
        
        # 배치
        self.full_subjects_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 버튼 프레임 추가
        button_frame = ttk.Frame(self.bottom_right_frame)
        button_frame.pack(side="bottom", fill="x", pady=5)

        # 더블클릭 이벤트 바인딩
        self.full_subjects_tree.bind("<Double-1>", lambda e: self.move_to_left())


    def create_timetable_term_1(self):
        # 시간표 프레임
        timetable_frame_term_1 = ttk.Frame(self.left_frame)
        timetable_frame_term_1.pack(side="left", fill="both", expand=True)

        # 요일 헤더
        for i, day in enumerate(self.days, start=1):
            ttk.Label(timetable_frame_term_1, text=day, width=10).grid(row=0, column=i)

        # 시간 슬롯
        for i, time in enumerate(self.time_slots):
            ttk.Label(timetable_frame_term_1, text=time, width=10).grid(row=i+1, column=0)
            
            # 각 시간대별 셀 생성
            for j in range(len(self.days)):
                cell_frame = ttk.Frame(timetable_frame_term_1, borderwidth=1, relief="solid")
                cell_frame.grid(row=i+1, column=j+1, padx=1, pady=1, sticky="nsew")
                
                # 과목명 라벨
                subject_label = ttk.Label(cell_frame, text="", width=10, wraplength=80)
                subject_label.pack(pady=2)
                
                # 셀 저장
                self.timetable_cells_term_1[(j, i)] = subject_label

    def create_timetable_term_2(self):
        timetable_frame_term_2 = ttk.Frame(self.right_frame)
        timetable_frame_term_2.pack(side="left", fill="both", expand=True)

        # 요일 헤더
        for i, day in enumerate(self.days, start=1):
            ttk.Label(timetable_frame_term_2, text=day, width=10).grid(row=0, column=i)

        # 시간 슬롯
        for i, time in enumerate(self.time_slots):
            ttk.Label(timetable_frame_term_2, text=time, width=10).grid(row=i+1, column=0)

            for j in range(len(self.days)):
                cell_frame = ttk.Frame(timetable_frame_term_2, borderwidth=1, relief="solid")
                cell_frame.grid(row=i+1, column=j+1, padx=1, pady=1, sticky="nsew")
                
                # 과목명 라벨
                subject_label = ttk.Label(cell_frame, text="", width=10, wraplength=80)
                subject_label.pack(pady=2)

                self.timetable_cells_term_2[(j, i)] = subject_label

    def create_current_credits(self):
        current_credits_frame = ttk.Frame(self.left_frame)
        current_credits_frame.pack(side="right", fill="both", expand=True)

        self.current_credits_label = ttk.Label(current_credits_frame, text="현재 추가된 학점: 0")
        self.current_credits_label.pack()
        

    def parse_time_slot(self, time_str):
        """강의 시간 문자열을 파싱하여 요일과 교시 인덱스 반환 (예: '월 1,2,3')"""
        try:
            day, periods = time_str.split()
            day_idx = self.day_map[day]
            
            # 교시 문자열을 인덱스 리스트로 변환
            period_indices = []
            for period in periods.split(','):
                period_idx = int(period) - 1  # 1교시는 인덱스 0
                if 0 <= period_idx < len(self.time_slots):
                    period_indices.append(period_idx)
                    print(period_idx)
            if period_indices:
                return day_idx, min(period_indices), max(period_indices)
            return None, None, None
            
        except Exception as e:
            print(f"시간 파싱 오류: {e}")
            return None, None, None

    def update_timetable_term_1(self):
        """추가된 과목 테이블의 데이터로 시간표 업데이트"""
        # 시간표 초기화
        for cell in self.timetable_cells_term_1.values():
            cell.configure(text="")
        self.cell_subject_map_term_1.clear()

        # 추가된 과목 테이블의 모든 항목 가져오기
        for item in self.added_subjects_tree.get_children():
            term = self.added_subjects_tree.item(item)['values'][10]
            if term == 1 or term == 'None':
                values = self.added_subjects_tree.item(item)['values']
                subject_name = values[3]  # 과목명
                time_str_1 = values[7]      # 강의 시간 (예: "월 1,2,3")
                time_str_2 = values[8]
                day_idx_1, start_idx_1, end_idx_1 = self.parse_time_slot(time_str_1)

                if None in (day_idx_1, start_idx_1, end_idx_1):
                    continue
                # 해당 교시 셀에 과목명 표시
                for i in range(start_idx_1, end_idx_1 + 1):
                    cell_key = (day_idx_1, i)
                    if cell_key in self.timetable_cells_term_1:
                        self.timetable_cells_term_1[cell_key].configure(text=subject_name)
                        self.cell_subject_map_term_1[cell_key] = values
                if time_str_2 != 'None':
                    day_idx_2, start_idx_2, end_idx_2 = self.parse_time_slot(time_str_2)
                    for i in range(start_idx_2, end_idx_2 + 1):
                        cell_key = (day_idx_2, i)
                        if cell_key in self.timetable_cells_term_1:
                            self.timetable_cells_term_1[cell_key].configure(text=subject_name)
                            self.cell_subject_map_term_1[cell_key] = values


    def update_timetable_term_2(self):
        """추가된 과목 테이블의 데이터로 시간표 업데이트"""
        # 시간표 초기화
        for cell in self.timetable_cells_term_2.values():
            cell.configure(text="")
        self.cell_subject_map_term_2.clear()

        # 추가된 과목 테이블의 모든 항목 가져오기
        for item in self.added_subjects_tree.get_children():
            term = self.added_subjects_tree.item(item)['values'][10]
            if term == 2 or term == 'None':
                values = self.added_subjects_tree.item(item)['values']
                subject_name = values[3]  # 과목명
                time_str_1 = values[7]      # 강의 시간 (예: "월 1,2,3")
                time_str_2 = values[8]
                day_idx_1, start_idx_1, end_idx_1 = self.parse_time_slot(time_str_1)
                if None in (day_idx_1, start_idx_1, end_idx_1):
                    continue
                # 해당 교시 셀에 과목명 표시
                for i in range(start_idx_1, end_idx_1 + 1):
                    cell_key = (day_idx_1, i)
                    if cell_key in self.timetable_cells_term_2:
                        self.timetable_cells_term_2[cell_key].configure(text=subject_name)
                        self.cell_subject_map_term_2[cell_key] = values
                if time_str_2 != 'None':
                    day_idx_2, start_idx_2, end_idx_2 = self.parse_time_slot(time_str_2)
                    for i in range(start_idx_2, end_idx_2 + 1):
                        cell_key = (day_idx_2, i)
                        if cell_key in self.timetable_cells_term_2:
                            self.timetable_cells_term_2[cell_key].configure(text=subject_name)
                            self.cell_subject_map_term_2[cell_key] = values

    def move_to_left(self):
        """과목을 왼쪽 테이블로 이동하고 시간표 업데이트"""
        selected_items = self.full_subjects_tree.selection()
        
        if not selected_items:
            return
            
        for item in selected_items:
            values = self.full_subjects_tree.item(item)['values']
            
            # 이미 추가된 강의인지 확인
            existing_items = self.added_subjects_tree.get_children()
            already_added = False
            
            for existing in existing_items:
                if self.added_subjects_tree.item(existing)['values'][4][:5] == values[4][:5]:  # 과목번호로 비교
                    already_added = True
                    break
                
            for existing in existing_items:
                if self.added_subjects_tree.item(existing)['values'][10] == values[10]:
                    if self.added_subjects_tree.item(existing)['values'][7][0] == values[7][0]:
                        if values[8] != 'None':
                            if self.added_subjects_tree.item(existing)['values'][8][0] == values[8][0]:
                                for time in self.added_subjects_tree.item(existing)['values'][7][2:].split(','):
                                    if time in values[7][2:].split(','):
                                        already_added = True
                                        print("파기")
                                        print(f"첫번째 {time}")
                                        return
                                for time in self.added_subjects_tree.item(existing)['values'][8][2:].split(','):
                                    if time in values[8][2:].split(','):
                                        already_added = True
                                        print("파기")
                                        print(f"두번째 {time}")
                                        return
                        else:
                            for time in self.added_subjects_tree.item(existing)['values'][7][2:].split(','):
                                if time in values[7][2:].split(','):
                                    already_added = True
                                    print("파기")
                                    print(f"첫번째 {time}")
                                    return
                            

            if not already_added:
                # 좌측 트리뷰에 추가 (정원 제외하고 추가)
                self.added_subjects_tree.insert("", "end", values=values[:])

        self.update_timetable_term_1()
        self.update_timetable_term_2()
        self.update_current_credits()

    def remove_from_left(self):
        # 선택된 항목 가져오기
        selected_items = self.added_subjects_tree.selection()
        
        if not selected_items:
            return
            
        # 선택된 항목 삭제
        for item in selected_items:
            self.added_subjects_tree.delete(item)

        self.update_timetable_term_1()
        self.update_timetable_term_2()
        self.update_current_credits()
        
    def update_current_credits(self):
        total_credits = 0
        if self.added_subjects_tree.get_children():
            for item in self.added_subjects_tree.get_children():
                values = self.added_subjects_tree.item(item)['values']
                total_credits += float(values[5])
        self.current_credits_label.configure(text=f"현재 추가된 학점: {total_credits}")


if __name__ == "__main__":
    root = tk.Tk()
    app = MainGUI(root)
    root.mainloop()




