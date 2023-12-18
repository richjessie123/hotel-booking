import pandas as pd

df = pd.read_csv("hotels.csv", dtype={"id": str})
dict_cards = pd.read_csv("cards.csv", dtype=str).to_dict(orient="records")
df_card_security = pd.read_csv("card_security.csv", dtype=str)


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


class SpaReservation(ReservationTicket):
    def generate(self):
        content = f"""
                Thank you for your SPA reservation!
                Here is your SPA booking data:
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
        if card_data in dict_cards:
            return True
        else:
            return False


class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
        password = df_card_security.loc[df_card_security["number"] == self.number, "password"].squeeze()
        if password == given_password:
            return True
        else:
            return False


print(df)
hotel_ID = input("Enter hotel id: ")
hotel = Hotel(hotel_ID)

if hotel.available():
    credit_card = SecureCreditCard(number="1234567890123456")
    if credit_card.validate(expiration="12/26", cvc="123", holder="JOHN SMITH"):
        if credit_card.authenticate(given_password="mypass"):
            hotel.book()
            name = input("Enter your name: ")
            reservation_ticket = ReservationTicket(customer_name=name, hotel_object=hotel)
            print(reservation_ticket.generate())
            spa_booking = input("Do you want to book a spa package? ")
            if spa_booking == "yes":
                spa_reservation = SpaReservation(customer_name=name, hotel_object=hotel)
                print(spa_reservation.generate())
            else:
                print("Enjoy your stay!")
        else:
            print("Credit Card authentication failed.")
    else:
        print("There is an issue with your payment")
else:
    print("Hotel is not available")
