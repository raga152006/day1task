import re
from config import COURSE_FEES, QUESTIONS


def workflow(question):

    # Find course codes such as CS101, AI202, DS303
    codes = re.findall(r"[A-Z]{2}\d{3}", question.upper())

    # Get the fees for the detected courses
    fees = [
        COURSE_FEES[code]
        for code in codes
        if code in COURSE_FEES
    ]

    # If no valid course was found
    if not fees:
        return "Sorry, I can only answer questions about course fees."

    text = question.lower()

    # Handle total fee questions
    if "total" in text:

        total = sum(fees)

        # Check for scholarship percentage
        percent = re.search(r"(\d+)\s*%", text)

        if "scholarship" in text and percent:
            total = total * (
                1 - int(percent.group(1)) / 100
            )

        return f"Total fee: Rs. {total:,.0f}"

    # Handle a single course fee
    if len(fees) == 1:
        return f"Fee for {codes[0]}: Rs. {fees[0]:,}"

    # Question type isn't supported by our rules
    return "Sorry, I do not have a rule for this type of question."


if __name__ == "__main__":

    print("\n=== SYSTEM 2: RULE-BASED WORKFLOW (no LLM) ===\n")

    for question in QUESTIONS:
        print("Q:", question)
        print("A:", workflow(question))
        print("-" * 70)