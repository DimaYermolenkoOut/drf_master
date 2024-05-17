from datetime import timedelta
from decimal import Decimal


from authentication.models import User

import graphene
from graphene_django import DjangoObjectType
from drfcalendar.models import Booking, Service, MasterSchedule
from expenses.models import Expense
from income.models import Income


class UserType(DjangoObjectType):
    class Meta:
        model = User

class IncomeType(DjangoObjectType):
    class Meta:
        model = Income


class ExpenseType(DjangoObjectType):
    class Meta:
        model = Expense


class ServiceType(DjangoObjectType):
    class Meta:
        model = Service

    def resolve_duration(self, info, **kwargs):
        hours, remainder = divmod(self.duration.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        total_minutes = hours * 60 + minutes
        return total_minutes


class MasterScheduleType(DjangoObjectType):
    class Meta:
        model = MasterSchedule


class BookingType(DjangoObjectType):
    class Meta:
        model = Booking

    master = graphene.Field(UserType)
    client = graphene.Field(UserType)
    service = graphene.Field(ServiceType)

    def resolve_master(self, info):
        return self.master

    def resolve_client(self, info):
        return self.client

    def resolve_service(self, info):
        return self.service


class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hi!")
    all_services = graphene.List(ServiceType)
    all_master_schedules = graphene.List(MasterScheduleType)
    all_bookings = graphene.List(BookingType)
    all_users = graphene.List(UserType)
    all_expenses = graphene.List(ExpenseType)
    all_incomes = graphene.List(IncomeType)

    def resolve_all_services(self, info, **kwargs):
        return Service.objects.all()

    def resolve_all_master_schedules(self, info, **kwargs):
        return MasterSchedule.objects.all()

    def resolve_all_bookings(self, info, **kwargs):
        return Booking.objects.all()

    def resolve_all_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_all_expenses(self, info):
        return Expense.objects.all()

    def resolve_all_incomes(self, info):
        return Income.objects.all()


########################### MUTATIONS ################################


class CreateBooking(graphene.Mutation):
    class Arguments:
        master_id = graphene.ID()
        start_time = graphene.DateTime()
        end_time = graphene.DateTime()
        client_id = graphene.ID()
        service_id = graphene.ID()

    booking = graphene.Field(BookingType)

    def mutate(self, info, master_id, start_time, end_time, client_id, service_id):
        master = UserType.get_node(info, master_id)
        client = UserType.get_node(info, client_id)
        service = ServiceType.get_node(info, service_id)
        booking = Booking(master=master, start_time=start_time, end_time=end_time, client=client, service=service)
        booking.save()
        return CreateBooking(booking=booking)


class CreateService(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        duration = graphene.Int()

    service = graphene.Field(ServiceType)

    def mutate(self, info, name, duration):
        service = Service(name=name, duration=timedelta(minutes=duration))
        service.save()
        return CreateService(service=service)


class CreateExpense(graphene.Mutation):
    class Arguments:
        category = graphene.String()
        amount = graphene.String()
        owner_id = graphene.ID()
        date = graphene.Date()
        description = graphene.String()

    expense = graphene.Field(ExpenseType)

    def mutate(self, info, category, amount, owner_id, date, description):
        owner = UserType.get_node(info, owner_id)
        # Конвертуємо значення amount у Decimal
        amount_decimal = Decimal(amount)
        expense = Expense(category=category, amount=amount_decimal, owner=owner, date=date,
                          description=description)
        expense.save()
        return CreateExpense(expense=expense)


class CreateIncome(graphene.Mutation):
    class Arguments:
        source = graphene.String()
        amount = graphene.String()
        owner_id = graphene.ID()
        date = graphene.Date()
        description = graphene.String()

    income = graphene.Field(IncomeType)

    def mutate(self, info, source, amount, owner_id, date, description):
        # Отримання власника доходу за його ідентифікатором
        owner = UserType.get_node(info, owner_id)
        amount_decimal = Decimal(amount)
        # Створення нового доходу і збереження його в базу даних
        income = Income(source=source, amount=amount_decimal, owner=owner, date=date,
                        description=description)
        income.save()

        # Повертаємо створений дохід
        return CreateIncome(income=income)


class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String()
        email = graphene.String()
        phone = graphene.String()
        is_verified = graphene.Boolean()
        is_active = graphene.Boolean()
        is_staff = graphene.Boolean()

    user = graphene.Field(UserType)

    def mutate(self, info, username, email, phone=None, is_verified=False, is_active=True,
               is_staff=False):
        # Створення нового користувача
        user = User.objects.create(username=username, email=email, phone=phone,
                                   is_verified=is_verified, is_active=is_active, is_staff=is_staff)

        # Повертаємо створеного користувача
        return CreateUser(user=user)


class CreateMasterSchedule(graphene.Mutation):
    class Arguments:
        master_id = graphene.ID(required=True)
        working_days = graphene.List(graphene.Int, required=True)
        start_time = graphene.Time(required=True)
        end_time = graphene.Time(required=True)

    master_schedule = graphene.Field(MasterScheduleType)

    def mutate(self, info, master_id, working_days, start_time, end_time):
        # Створення нового об'єкта MasterSchedule
        master_schedule = MasterSchedule.objects.create(master_id=master_id,
                                                        working_days=working_days,
                                                        start_time=start_time, end_time=end_time)

        # Повернення створеного об'єкта MasterSchedule
        return CreateMasterSchedule(master_schedule=master_schedule)



class Mutation(graphene.ObjectType):
    create_service = CreateService.Field()
    create_booking = CreateBooking.Field()
    create_expense = CreateExpense.Field()
    create_master_schedule = CreateMasterSchedule.Field()
    create_income = CreateIncome.Field()
    create_user = CreateUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)


###################Services################
# {
#   allServices {
#     id
#     name
#     duration
#   }
# }
# {
#   "data": {
#     "allServices": [
#       {
#         "id": "2",
#         "name": "less-2 90",
#         "duration": 90
#       },
#       {
#         "id": "1",
#         "name": "less-1 60",
#         "duration": 60
#       }
#     ]
#   }
# }

################Booking graphql################
# {
#   allBookings {
#     id
#     startTime
#     service {
#       id
#     }
#     client {
#       id
#       username
#       # Інші поля про клієнта, які вам потрібні
#     }
#   }
# }
##########################Users###################
# {
#   allUsers{
#     id
#     username
#     phone
#     email
#
#   }
# }
########################Expenses###################
# {
#   allExpenses {
#     id
#     category
#     amount
#     owner {
#       id
#       email
#     }
#     date
#     description
#   }
# }
# ############################INCOME################
# {
#   allIncomes {
#     id
#     source
#     amount
#     owner {
#       id
#       email
#     }
#     date
#     description
#   }
# }

########### MUTATIONS ################
# mutation {
#   createBooking(
#     masterId: "8",
#     startTime: "2024-05-17T08:00:00Z",
#     endTime: "2024-05-17T09:00:00Z",
#     clientId: "7",
#     serviceId: "1"
#   ) {
#     booking {
#       id
#       startTime
#       endTime
#       master {
#         id
#       }
#       client {
#         id
#       }
#       service {
#         id
#       }
#     }
#   }
# }
###########Service create
# mutation {
#   createService(
#     name: "Less - 120",
#     duration: 120
#   ) {
#     service {
#       id
#       name
#       duration
#     }
#   }
# }

############Expense create
# mutation {
#   createExpense(
#     category: "FOOD",
#     amount: "100",
#     ownerId: "8",
#     date: "2024-05-17",
#     description: "some description"
#   ) {
#     expense {
#       id
#       category
#       amount
#       owner {
#         id
#       }
#       date
#       description
#     }
#   }
# }
##################### Income create
# mutation {
#   createIncome(
#     source: "SALARY",
#     amount: "100.0",
#     ownerId: "8",
#     date: "2024-05-17",
#     description: "some description"
#   ) {
#     income {
#       id
#       source
#       amount
#       owner {
#         id
#       }
#       date
#       description
#     }
#   }
# }
################### User create
# mutation {
#   createUser(
#     username: "test",
#     email: "test@example.com",
#     isVerified: true,
#     isActive: true,
#     isStaff: false
#   ) {
#     user {
#       id
#       username
#       email
#     }
#   }
# }
################# MasterSchedule create
# mutation {
#   createMasterSchedule(
#     masterId: "9",
#     workingDays: [1, 2, 3, 4, 5],
#     startTime: "08:00:00",
#     endTime: "17:00:00"
#   ) {
#     masterSchedule {
#       id
#       master {
#         id
#         email
#       }
#       workingDays
#       startTime
#       endTime
#     }
#   }
# }