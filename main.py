import pandas as pd

df = pd.read_csv("hotels.csv", dtype={"id": str})
df_cards = pd.read_csv("cards.csv", dtype=str).to_dict(orient="records")


class Hotel:

    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()

    def available(self):
        """Check if a hotel is available"""
        availability = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        if availability == "yes":
            return True
        else:
            return False

    def book(self):
        """Book a hotel by changing its availability to now"""
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False)


class ReservationTicket:
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel_object = hotel_object

    def generate(self):
        content = f"""
        Thank you for your reservation!
        Here is your booking data:
        Name: {self.customer_name}
        Hotel name: {self.hotel_object.name}
        """
        return content


class CreditCard:
    def __init__(self, number):
        self.number = number

    def validate(self, expiration, cvc, holder):
        card_data = {"number": self.number, "expiration": expiration,
                     "cvc": cvc, "holder": holder}
        if card_data in df_cards:
            return True
        else:
            return False


print(df)
hotel_ID = input("Enter hotel id: ")
hotel = Hotel(hotel_ID)

if hotel.available():
    credit_card = CreditCard(number="1234567890123456")
    if credit_card.validate(expiration="12/26", cvc="123", holder="JOHN SMITH"):
        hotel.book()
        name = input("Enter your name: ")
        reservation_ticket = ReservationTicket(customer_name=name, hotel_object=hotel)
        print(reservation_ticket.generate())
    else:
        print("There is an issue with your payment")
else:
    print("Hotel is not available")
