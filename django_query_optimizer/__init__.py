from .query_optimizer import QueryOptimizer

def optimize_query(model):
    query_optimizer = QueryOptimizer(model)
    return query_optimizer.optimize_query()