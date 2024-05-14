import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError

from users.schema import UserType
from divisas.models import Divisa, Vote

class DivisaType(DjangoObjectType):
    class Meta:
        model = Divisa

class VoteType(DjangoObjectType):
    class Meta:
        model = Vote

class Query(graphene.ObjectType):
    divisas = graphene.List(DivisaType)
    votes = graphene.List(VoteType)

    def resolve_divisas(self, info, **kwargs):
        return Divisa.objects.all()
    
    def resolve_votes(self, info, **kwargs):
        return Vote.objects.all()
    
class CreateDivisa(graphene.Mutation):
    id = graphene.Int()
    nombre = graphene.String()
    pais = graphene.String()
    acronimo = graphene.String()
    precio = graphene.Float()
    posted_by = graphene.Field(UserType)

    class Arguments:
       nombre = graphene.String()
       pais = graphene.String()
       acronimo = graphene.String()
       precio = graphene.Float() 

    def mutate(self, info, nombre, pais, acronimo, precio):
        user = info.context.user or None

        divisa = Divisa(
            nombre=nombre,
            pais=pais,
            acronimo=acronimo,
            precio=precio,
            posted_by=user,
        )
        divisa.save()

        return CreateDivisa(
            id=divisa.id,
            nombre=divisa.nombre,
            pais=divisa.pais,
            acronimo=divisa.acronimo,
            precio=divisa.precio,
            posted_by=divisa.posted_by,
        )
    
class CreateVote(graphene.Mutation):
    user = graphene.Field(UserType)
    divisa = graphene.Field(DivisaType)

    class Arguments:
        divisa_id = graphene.Int()

    def mutate(self, info, divisa_id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('Debes estar loggeado para votar')

        divisa = Divisa.objects.filter(id=divisa_id).first()
        if not divisa:
            raise GraphQLError('Divisa invalida')

        Vote.objects.create(
            user=user,
            divisa=divisa,
        )

        return CreateVote(user=user, divisa=divisa)

    
class Mutation(graphene.ObjectType):
    create_divisa = CreateDivisa.Field()
    create_vote = CreateVote.Field()
