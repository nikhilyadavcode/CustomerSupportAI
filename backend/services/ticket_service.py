from database.connection import tickets_collection
import uuid


def get_all_tickets():

    tickets = list(
        tickets_collection.find(
            {},
            {"_id": 0}
        )
    )

    return tickets


def find_ticket(ticket_id: str):

    ticket = tickets_collection.find_one(
        {"ticket_id": ticket_id},
        {"_id": 0}
    )

    return ticket


def create_ticket(customer, email, issue, description):

    ticket = {
        "ticket_id": "T" + str(uuid.uuid4())[:8].upper(),
        "customer": customer,
        "email": email,
        "issue": issue,
        "description": description,
        "status": "Open",
        "priority": "High"
    }

    tickets_collection.insert_one(ticket)

    return ticket