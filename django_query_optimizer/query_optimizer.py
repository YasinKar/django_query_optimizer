from django.db.models import Model, QuerySet
from .model_analyzer import ModelAnalyzer

class QueryOptimizer:
    def __init__(self, model: type[Model]):
        """
        Initialize the QueryOptimizer with a model.

        :param model: The Django model class.
        """
        if not issubclass(model, Model):
            raise TypeError("The input must be a Django model class.")
        
        self.model = model
        self.analyzer = ModelAnalyzer(model)  # Initialize ModelAnalyzer
        
    def optimize_query(self) -> QuerySet:
        """
        Optimize query based on relationships (direct or reverse).
        """
        queryset = self.model.objects.all()

        # Analyze relations and optimize if needed
        if self.analyzer.has_relations():
            relations = self.analyzer.analyze_relations()

            # Apply select_related
            if relations['select_related']:
                queryset = queryset.select_related(*relations['select_related'])

            # Apply prefetch_related
            if relations['prefetch_related']:
                queryset = queryset.prefetch_related(*relations['prefetch_related'])

        return queryset