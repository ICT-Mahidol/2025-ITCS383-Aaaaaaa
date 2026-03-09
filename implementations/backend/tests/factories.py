import factory
from app.models.user import User, UserRole
from app.models.event import Event
from app.models.booth import Booth, BoothType, BoothClassification, DurationType
from app.models.merchant import Merchant
from app.models.reservation import Reservation, ReservationType
from app.models.payment import Payment, PaymentMethod
from app.services.auth_service import get_password_hash

class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.Faker('uuid4')
    username = factory.Faker('user_name')
    password = factory.LazyFunction(lambda: get_password_hash("testpass"))
    name = factory.Faker('name')
    citizen_id = factory.Faker('ssn')
    contact_info = factory.Faker('email')
    role = UserRole.GENERAL_USER

class EventFactory(factory.Factory):
    class Meta:
        model = Event

    event_id = factory.Faker('uuid4')
    name = factory.Faker('sentence', nb_words=3)
    description = factory.Faker('text')
    location = factory.Faker('address')
    start_date = factory.Faker('date_this_year')
    end_date = factory.Faker('date_this_year')
    created_by = factory.Faker('uuid4')

class BoothFactory(factory.Factory):
    class Meta:
        model = Booth

    booth_id = factory.Faker('uuid4')
    event_id = factory.Faker('uuid4')
    booth_number = factory.Faker('bothify', text='A##')
    size = factory.Faker('random_element', elements=['Small', 'Medium', 'Large'])
    price = factory.Faker('pydecimal', left_digits=3, right_digits=2, positive=True)
    location = factory.Faker('address')
    type = BoothType.INDOOR
    classification = BoothClassification.TEMPORARY
    duration_type = DurationType.SHORT_TERM

class MerchantFactory(factory.Factory):
    class Meta:
        model = Merchant

    merchant_id = factory.Faker('uuid4')
    user_id = factory.Faker('uuid4')
    seller_information = factory.Faker('text')
    product_description = factory.Faker('text')

class ReservationFactory(factory.Factory):
    class Meta:
        model = Reservation

    reservation_id = factory.Faker('uuid4')
    booth_id = factory.Faker('uuid4')
    merchant_id = factory.Faker('uuid4')
    reservation_type = ReservationType.SHORT_TERM

class PaymentFactory(factory.Factory):
    class Meta:
        model = Payment

    payment_id = factory.Faker('uuid4')
    reservation_id = factory.Faker('uuid4')
    amount = factory.Faker('pydecimal', left_digits=3, right_digits=2, positive=True)
    method = PaymentMethod.CREDIT_CARD