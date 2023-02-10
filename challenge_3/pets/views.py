from rest_framework.views import APIView, Request, Response, status
from rest_framework.pagination import PageNumberPagination
from .models import Pet
from .serializers import PetSerializer
from traits.models import Trait
from groups.models import Group
from django.shortcuts import get_object_or_404


class PetView(APIView, PageNumberPagination):
    def get(self, request: Request) -> Response:
        pets = Pet.objects.all()

        trait = request.query_params.get("trait")
        if trait:
            pets = pets.filter(traits__name__iexact=trait)

        pets_page = self.paginate_queryset(pets, request)
        pet_serializer = PetSerializer(pets_page, many=True)

        return self.get_paginated_response(pet_serializer.data)

    def post(self, request: Request) -> Response:
        pet_serializer = PetSerializer(data=request.data)
        pet_serializer.is_valid(raise_exception=True)

        group_data = pet_serializer.validated_data.pop("group")
        trait_list = pet_serializer.validated_data.pop("traits")

        try:
            group = Group.objects.get(
                scientific_name__iexact=group_data["scientific_name"]
            )
        except Group.DoesNotExist:
            group = Group.objects.create(**group_data)

        create_pet = Pet.objects.create(**pet_serializer.validated_data, group=group)

        for trait in trait_list:
            try:
                traits = Trait.objects.get(name__iexact=trait["name"])
            except Trait.DoesNotExist:
                traits = Trait.objects.create(**trait)

            create_pet.traits.add(traits)

        pet_serializer = PetSerializer(create_pet)

        return Response(pet_serializer.data, status.HTTP_201_CREATED)


class PetIdView(APIView):
    def get(self, request: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)
        pet_serializer = PetSerializer(pet)

        return Response(pet_serializer.data)

    def patch(self, request: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)

        pet_serializer = PetSerializer(data=request.data, partial=True)
        pet_serializer.is_valid(raise_exception=True)

        group_data: dict = pet_serializer.validated_data.pop("group", None)
        trait_list = pet_serializer.validated_data.pop("traits", None)

        if group_data:
            try:
                group = Group.objects.get(
                    scientific_name__iexact=group_data["scientific_name"]
                )
            except Group.DoesNotExist:
                group = Group.objects.create(**group_data)
            pet.group = group
            pet.save()

        if trait_list:
            pet.traits.clear()
            for trait in trait_list:
                try:
                    traits = Trait.objects.get(name__iexact=trait["name"])
                except Trait.DoesNotExist:
                    traits = Trait.objects.create(**trait)
                pet.traits.add(traits)

        for key, value in pet_serializer.validated_data.items():
            setattr(pet, key, value)
        pet.save()

        pet_serializer = PetSerializer(pet)
        return Response(pet_serializer.data)

    def delete(self, request: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)
        pet.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
