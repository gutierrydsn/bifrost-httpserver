# Bifrost HttpServer

   This library was created to facilitate the development of web services adopting 
   the market standard. Using a mapping file of routes in this way defining the 
   method to be published.
   

### Installation

Requires python 3 and pip for install.

```sh
pip install bifrost-<ver>.tar.gz
```

example:

```sh
pip install bifrost-0.1.tar.gz
```

### Use examples

use with module

* * [Use examples]
```sh
python -m bifrost.http_server
```

in the folder where the server will run must contain at least two files, the routing file and a controller.
The route file contains the mapping of the endpoints to the methods to be executed from a controller.
The controller contains the class where the methods that will respond to the request will be implemented.

example file routes:



```json
{
	"GET" : {
    	"/teste" : "controller.classe.teste()"
    },
    
    "POST" : {
    	"/salvar_teste" : "controller.classe.salvar()"
    }
}
```


example file controller.py:


```python
class classe():
	def teste():
    	return '{"return": "teste"}'
     
    def salvar():
    	...
    	return '"return" : "Salvo com sucesso!"'
```

[Use examples]: <samples/>