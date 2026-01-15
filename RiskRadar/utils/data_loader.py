import json

def load_business_data(path):
    with open(path, "r") as f:
        data = json.load(f)

    texts = []
    for entry in data:
        text = (
            f"Business: {entry['business_name']}, "
            f"Type: {entry['business_type']}, "
            f"Established: {entry['year_established']}, "
            f"Annual Revenue: {entry['annual_revenue']}, "
            f"Profit Margin: {entry['profit_margin']}, "
            f"Loan History: {entry['loan_history']}, "
            f"GST Compliant: {entry['gst_compliant']}, "
            f"Negative News: {entry['negative_news']}, "
            f"Rating: {entry['rating']}, "
            f"Notes: {entry['notes']}"
        )
        texts.append(text)

    return data, texts
