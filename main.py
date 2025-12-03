class SimpleStudyPlanner:
    def __init__(self):
        # รายชื่อวิชาที่ต้องจัดตารางอ่าน
        self.subjects = [
            "INT130 Computing Platform Basics",
            "INT143 Software Process Fundamentals",
            "INT140 Computational Thinking",
            "INT120 UX/UI Design Fundamentals",
            "INT101 Discrete Mathematics",
        ]

        # ใช้ Abstraction เก็บข้อมูลของวิชาในรูปแบบ dictionary
        self.difficulty = {}   
        self.readiness = {}    
        self.weights = {}      
        self.ideal_hours = {}  

        self.daily_hours = [0] * 7

        self.schedule = [{} for _ in range(7)]

        # ชื่อวันแบบภาษาไทย ใช้ Pattern Recognition
        self.day_names = [
            "วันจันทร์", "วันอังคาร", "วันพุธ",
            "วันพฤหัสบดี", "วันศุกร์", "วันเสาร์", "วันอาทิตย์"
        ]
        

        self.day_to_index = {
            "วันจันทร์": 0,
            "วันอังคาร": 1,
            "วันพุธ": 2,
            "วันพฤหัสบดี": 3,
            "วันศุกร์": 4,
            "วันเสาร์": 5,
            "วันอาทิตย์": 6
        }

    # แปลงจำนวนชั่วโมงเป็นข้อความอ่านง่าย เช่น "2 ชั่วโมง 30 นาที"
    def format_hours(self, hours):
        h = int(hours)
        m = int(round((hours - h) * 60))

        # ป้องกันกรณีนาทีขึ้นเป็น 60
        if m == 60:
            h += 1
            m = 0

        if h > 0 and m > 0:
            return f"{h} ชั่วโมง {m} นาที"
        elif h > 0 and m == 0:
            return f"{h} ชั่วโมง"
        elif h == 0 and m > 0:
            return f"{m} นาที"
        else:
            return "0 นาที"

    # รับข้อมูลเวลาว่างในแต่ละวันจากผู้ใช้
    def input_daily_hours(self):
        print("กรอกเวลาว่างในวันที่อ่านหนังสือได้ (พิมพ์: ชื่อวัน ชั่วโมง)")
        print("ตัวอย่าง: วันจันทร์ 3")
        print("พิมพ์ 'done' เพื่อจบ")
        print("หมายเหตุ: ชั่วโมงต้องไม่เกิน 24\n")

        while True:
            user_input = input("> ").strip()

            # จบการกรอกข้อมูล
            if user_input.lower() == "done":
                break

            try:
                # แยกข้อมูลเป็นชื่อวันและจำนวนชั่วโมง
                parts = user_input.split()
                if len(parts) != 2:
                    raise ValueError("รูปแบบต้องเป็น: ชื่อวัน ชั่วโมง")

                day_name = parts[0]
                hours = float(parts[1])

                # ตรวจสอบชื่อวัน
                if day_name not in self.day_to_index:
                    raise ValueError("ชื่อวันไม่ถูกต้อง (เช่น วันจันทร์ วันศุกร์ เป็นต้น)")

                # ตรวจสอบจำนวนชั่วโมง
                if hours < 0:
                    raise ValueError("เวลาต้องไม่เป็นค่าติดลบ")
                if hours > 24:
                    raise ValueError("เวลาต่อวันต้องไม่เกิน 24 ชั่วโมง")

                #
                day_index = self.day_to_index[day_name]
                self.daily_hours[day_index] = hours # type: ignore
                print(f"บันทึกแล้ว: {day_name} = {hours} ชั่วโมง")

            except ValueError as e:
                print("⚠ ข้อมูลผิดพลาด:", e)

        # แสดงข้อมูลสรุปทั้งหมด
        print("\nสรุปเวลาว่างต่อวัน:")
        for i, h in enumerate(self.daily_hours):
            print(f"{self.day_names[i]}: {h} ชั่วโมง")

    # รับข้อมูลคะแนนความยากและความพร้อมของแต่ละวิชา
    def input_subject_info(self):
        print("\nให้คะแนนแต่ละวิชา (1-5)")
        for subj in self.subjects:
            while True:
                try:
                    # รับคะแนนความยาก
                    d = int(input(f"[{subj}] ความยาก (1-5): "))
                    # รับคะแนนความพร้อม
                    r = int(input(f"[{subj}] ความพร้อม (1-5): "))

                    # ตรวจสอบช่วงคะแนน
                    if not (1 <= d <= 5 and 1 <= r <= 5):
                        raise ValueError

                    self.difficulty[subj] = d
                    self.readiness[subj] = r
                    break
                except ValueError:
                    print("คะแนนต้องเป็น 1-5")

    # คำนวณชั่วโมงที่เหมาะสมของแต่ละวิชา
    def compute_hours(self):
        total_free = sum(self.daily_hours)   # เวลาว่างรวมในสัปดาห์

        for subj in self.subjects:
            d = self.difficulty[subj]
            r = self.readiness[subj]

            # คำนวณน้ำหนัก: ยากมาก + ไม่พร้อมมาก -> weight สูง
            w = d * (6 - r)
            self.weights[subj] = max(w, 1)   # ป้องกัน weight = 0

        total_weight = sum(self.weights.values())

        # คำนวณชั่วโมงตามสัดส่วนของน้ำหนัก
        for subj in self.subjects:
            self.ideal_hours[subj] = (
                total_free * (self.weights[subj] / total_weight)
            )

    # กระจายชั่วโมงอ่านหนังสือลงในแต่ละวันตามเวลาว่าง
    def distribute(self):
        remaining = {s: h for s, h in self.ideal_hours.items()}  # ชั่วโมงที่ยังต้องจัดให้แต่ละวิชา

        for day_i in range(7):
            capacity = self.daily_hours[day_i]   # ความจุเวลาว่างของวันนั้น

            if capacity <= 0:
                continue

            # จัดชั่วโมงให้วิชาตามลำดับ
            for subj in self.subjects:
                if remaining[subj] <= 0:
                    continue

                # ส่งให้มากที่สุดโดยไม่เกิน capacity
                assign = min(remaining[subj], capacity)
                self.schedule[day_i][subj] = assign

                # ปรับค่าที่เหลือ
                remaining[subj] -= assign
                capacity -= assign

                # ถ้าเวลาว่างของวันหมด ให้ไปวันถัดไป
                if capacity <= 0:
                    break

    # แสดงตารางอ่านหนังสือรายวัน
    def print_schedule(self):
        print("\n============= ตารางอ่านหนังสือ =============\n")
        for i, day_plan in enumerate(self.schedule):
            print(self.day_names[i] + ":")
            if not day_plan:
                print("  - ไม่มีการอ่าน")
            else:
                for subj, hrs in day_plan.items():
                    print(f"  - {subj}: {self.format_hours(hrs)}")
            print()

        print("============================================")
        print("ชั่วโมงต่อวิชา (รวม):")
        for subj in self.subjects:
            print(f"- {subj}: {self.format_hours(self.ideal_hours[subj])}")
        print()

    # ฟังก์ชันหลักที่ควบคุมลำดับการทำงานทั้งหมด
    def run(self):
        print("=== Study Planner (เพิ่มกรอกวันที่ว่างเอง + ชั่วโมงเป็นนาที) ===\n")
        self.input_daily_hours()
        self.input_subject_info()
        self.compute_hours()
        self.distribute()
        self.print_schedule()


if __name__ == "__main__":
    SimpleStudyPlanner().run()

    # Decomposition (การแยกส่วนของปัญหา) ทำการแยกฟังก์ชั่นต่างๆ ออกเป็นส่วนย่อยๆเพื่อให้ง่ายต่อการจัดการ 
    # 1) format_hours แปลงชั่วโมงเป็นรูปแบบที่อ่านง่าย
    # 2) input_daily_hours กรอกวันและเวลาว่างต่อวัน
    # 3) input_subject_info กรอกความยากและความพร้อมของแต่ละวิชา
    # 4) compute_hours คำนวณชั่วโมงที่เหมาะสม
    # 5) distribute แจกจ่ายชั่วโมงอ่านหนังสือต่อวัน
    # 6) print_schedule แสดงตารางอ่านหนังสือ