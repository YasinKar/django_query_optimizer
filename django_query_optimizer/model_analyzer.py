from django.db.models import (
    Model,
    Field,
    ForeignKey,
    OneToOneField,
    ManyToOneRel,
    ManyToManyRel
)
from django.contrib.contenttypes.fields import GenericRelation

class ModelAnalyzer:
    def __init__(self, model: type[Model]):
        # Validate that the input is a Django model class
        if not issubclass(model, Model):
            raise TypeError("The input must be a Django model class.")
        self.model = model
        
        self.relations = {
            'select_related': [],
            'prefetch_related': []
        }
        
    def get_fields(self):
        """Returns all fields of the model."""
        return self.model._meta.get_fields()

    def has_relations(self) -> bool:
        """Checks if the model has any relationships."""
        return any(field.is_relation for field in self.get_fields())

    def _analyze_nested_relations(self, field: Field,  relation_type: str):
        """Helper function to analyze nested relations."""
        if not field.is_relation:
            raise TypeError(f"The field '{field.name}' is not a relational field.")
        
        related_model: Model = field.related_model
        nested_relations = []
        for nested_field in related_model._meta.get_fields():
            if nested_field.is_relation:
                if relation_type == 'select_related':
                    if isinstance(nested_field, (ForeignKey, OneToOneField)):
                        nested_relations.append(f'{field.name}__{nested_field.name}')
                    
                else:
                    nested_relations.append(f'{field.name}__{nested_field.name}')
        return nested_relations

    def analyze_relations(self):
        """
        Returns a dictionary of related fields and their related names.
        Includes both direct and reverse relations.
        Supports nested relations.
        """

        for field in self.get_fields():
            # Direct relations (ForeignKey, OneToOneField)
            if isinstance(field, (ForeignKey, OneToOneField)):
                self.relations['select_related'].append(field.name)
                self.relations['select_related'] += self._analyze_nested_relations(field, 'select_related')

            # Many-to-Many relations
            elif isinstance(field, ManyToManyRel):
                self.relations['prefetch_related'].append(field.name)
                self.relations['prefetch_related'] += self._analyze_nested_relations(field, 'prefetch_related')

            # Reverse relations
            elif field.is_relation and field.auto_created and not field.concrete:
                if isinstance(field, ManyToOneRel):
                    self.relations['prefetch_related'].append(field.get_accessor_name())
                    self.relations['prefetch_related'] += self._analyze_nested_relations(field, 'prefetch_related')

            # Generic relations
            elif isinstance(field, GenericRelation):
                self.relations['prefetch_related'].append(field.name)

        print(self.relations)
        return self.relations