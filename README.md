# Django query optimizer

Automatic optimization of django queries

## Features

- analyze django models and identifies direct and reverce relations
- returns a query that allows you to apply your own filters


## Installation

- Install using pip:

```sh
$ pip install django_query_optimizer
```
- ```Dont``` add package to django ```INSTALLED_APPS```
## Usage

Django query optimizer is easy to use and you can just import it and assign your model to ```optimize_query```:

from django_query_optimizer import optimize_query
from .models import YourModel

def your_view(request):
    queryset = optimize_query(YourModel)
    context ={
        'objects' : queryset 
    }
        
    return render(request, "your_page.html", context)

And you can also apply your own filters:

from django_query_optimizer import optimize_query
from .models import YourModel

def detail_view(request, id):
    queryset = optimize_query(YourModel).get(id = id)
    context ={
        'object' : queryset 
    }
        
    return render(request, "detail_page.html", context)
    
Other example:

from django_query_optimizer import optimize_query
from .models import YourModel

def filters_view(request):
    queryset = optimize_query(YourModel).filter(is_active=True)
    context ={
        'objects' : queryset 
    }
        
    return render(request, "filters_page.html", context)

Was it useful for you? Leave a star ⭐⭐⭐ - 2024 Yasin Karbasi