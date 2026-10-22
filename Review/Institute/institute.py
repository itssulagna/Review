import csv
from datetime import datetime, date
today = date.today()
class course:
    def __init__(self, course_id, course_name, basefee,
                 offer_discount, offer_end_date):
        self.course_id = course_id
        self.course_name = course_name
        self.basefee = basefee
        self.offer_discount = offer_discount
        self.offer_end_date = offer_end_date

    def calculate_fee(self):
        return self.basefee

class classroomcourse(course):
    def __init__(self, course_id, course_name, basefee,offer_discount, offer_end_date):
        super().__init__(course_id, course_name, basefee,offer_discount, offer_end_date)
        self.course_type = "Classroom"

    def calculate_fee(self):
        adjusted_fee = self.basefee + 2000
        return adjusted_fee

class onlinecourse(course):
    def __init__(self, course_id, course_name, basefee,
                 offer_discount, offer_end_date):
        super().__init__(course_id, course_name, basefee,offer_discount, offer_end_date)
        self.course_type = "Online"

    def calculate_fee(self):
        discount = self.basefee * 0.10
        adjusted_fee = self.basefee - discount
        return adjusted_fee

valid_courses = []
valid_id = set()
rejected = 0
errors = []

try:
    with open("courses.csv", "r", newline="") as file:
        reader = csv.DictReader(file)

        for data in reader:
            course_id = data["CourseID"].strip()
            course_name = data["CourseName"].strip()
            course_type = data["CourseType"].strip()
            offer_discount = data["OfferDiscount"].strip()
            offer_end_date = data["OfferEndDate"].strip()

            if course_id == "":
                print("Invalid ID")
                errors.append(f"Record: {data} ====> Invalid ID")
                rejected += 1
                continue

            if course_id in valid_id:
                print("Duplicate ID")
                errors.append(f"Record: {data} ====> Duplicate ID")
                rejected += 1
                continue

            if course_name == "":
                print("Invalid course name")
                errors.append(f"Record: {data} ====> Invalid course name")
                rejected += 1
                continue

            if course_type not in ("Classroom", "Online"):
                print("Invalid course type")
                errors.append(f"Record: {data} ====> Invalid course type")
                rejected += 1
                continue

            try:
                basefee = float(data["BaseFee"])

            except ValueError:
                print("Invalid base fee")
                errors.append(f"Record: {data} ====> Invalid base fee")
                rejected += 1
                continue

            if basefee <= 0:
                print("Base fee must be greater than zero")
                errors.append(f"Record: {data} ====> Invalid base fee")
                rejected += 1
                continue

            try:
                offer_discount = float(offer_discount)

            except ValueError:
                print("Invalid offer discount")
                errors.append(f"Record: {data} ====> Invalid offer discount")
                rejected += 1
                continue

            if offer_discount < 0 or offer_discount > 100:
                print("Invalid offer discount")
                errors.append(f"Record: {data} ====> Discount must be between 0 and 100")
                rejected += 1
                continue

            if offer_end_date != "":
                try:
                    offer_end_date = datetime.strptime(
                        offer_end_date, "%Y-%m-%d"
                    ).date()

                except ValueError:
                    print("Invalid offer end date")
                    errors.append(
                        f"Record: {data} ====> Invalid offer end date"
                    )
                    rejected += 1
                    continue

            else:
                offer_end_date = None

            if course_type == "Classroom":
                obj = classroomcourse(course_id, course_name, basefee,offer_discount, offer_end_date)

            else:
                obj = onlinecourse(course_id, course_name, basefee,offer_discount, offer_end_date)

            valid_courses.append(obj)
            valid_id.add(course_id)

            print("Valid course:", course_id, course_name)

    report = []

    for obj in valid_courses:
        adjusted_fee = obj.calculate_fee()

        if (obj.offer_discount > 0 and
                obj.offer_end_date is not None and
                obj.offer_end_date >= today):

            offer_amount =((adjusted_fee * obj.offer_discount )/ 100)
            final_fee = adjusted_fee - offer_amount
            offer_status = "WithOffer"

        else:
            offer_amount = 0
            final_fee = adjusted_fee
            offer_status = "WithoutOffer"

        course_details = {
            "CourseID": obj.course_id,
            "CourseName": obj.course_name,
            "CourseType": obj.course_type,
            "BaseFee": obj.basefee,
            "CourseAdjustmentFee": adjusted_fee,
            "OfferDiscountPercent": obj.offer_discount,
            "OfferEndDate": (obj.offer_end_date if obj.offer_end_date else ""),
            "OfferStatus": offer_status,
            "OfferDiscountAmount": offer_amount,
            "FinalFee": final_fee
        }

        report.append(course_details)

        print(obj.course_name,adjusted_fee,offer_amount,final_fee,offer_status )


#final report
    with open("course_report.csv", "w", newline="") as file:
        fields = [
            "CourseID",
            "CourseName",
            "CourseType",
            "BaseFee",
            "CourseAdjustmentFee",
            "OfferDiscountPercent",
            "OfferEndDate",
            "OfferStatus",
            "OfferDiscountAmount",
            "FinalFee"
        ]

        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(report)

    print("\nCourse report generated successfully")


    with open("errors.txt", "w") as file:
        for error in errors:
            file.write(error + "\n")

    print("Error file generated successfully")

    # Summary
    total_final_fees = 0

    for item in report:
        total_final_fees += item["FinalFee"]

    print("\n----- COURSE FEE SUMMARY -----")
    print("Total valid courses:", len(valid_courses))
    print("Total rejected courses:", rejected)
    print("Combined final fees: ", round(total_final_fees, 2))

except FileNotFoundError:
    print("File does not exist: courses.csv")

