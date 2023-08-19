django-dynamic-host
==========================================================

Django dynamic host helps you validate hostname(origin of client) trying to reach your application dynamically. 
Django dynamic host helps by-pass the ALLOWED_HOST settings which is restricted to a constant manually added value of hostnames

For example, let's say you are building a distributed system where a number of dynamically registered (domain stored in database) frontend domain consumes your api.
It may become difficult adding them manually to ALLOWED_HOST list or creating different settings file for each. well that is where this library comes in handy.
What you can do in this case is simple.

* install the library

    .. code-block:: shell

        pip install django-dynamic-host

* add library to INSTALLED_APP and add AllowedHostMiddleWare to middleware. You should add the this middleware to the highest

    .. code-block:: python
        
        INSTALLED_APPS= [
            ...
            "dynamic_host",
        ]

        # notice middleware sits at the top... 
        MIDDLEWARE = [
            "dynamic_host.middleware.AllowedHostMiddleWare",
            ...
        ]
* disable allowed host by  adding a  ``*`` to ALLOWED_HOST in settings "this is so django-dynamic-host middleware can take responsibility for allowed_host " 

    .. code-block:: python
        
        ALLOWED_HOST=['*']

* write a simple resolver function that takes in host, request and extra kwargs just in case

    .. code-block:: python

        def some_function(host, request,**kwargs):
            """
                add some logic to check domain in database 
                or some inmemory database system... this is
                totally up to you
            """
            if cache.exists(host):
                return True
            elif Model.objects.filter(domain=host).exists():
                save_to_cache(host)
                return True
            return False 

* add path the function from settings.py like so


.. code-block:: python

    DYNAMIC_HOST_RESOLVER_FUNC="path.to.func"


Installation
----------------------------------------------------------

First, install the app with your favorite package manager, e.g.:

.. code-block:: shell

    pip install django-dynamic-host

Then configure your Django to use the app:

#. Add ``'dynamic_host'`` to your ``INSTALLED_APPS`` setting.

#. Add ``'dynamic_host.middleware.AllowedHostMiddleWare'`` to the
   **beginning** of your ``MIDDLEWARE`` setting.

#. **DISABLE** ``'ALLOWED_HOST'`` by setting it to ``'['*']'`` in settings.py so the middleware takes responsibility of checking if host is valid.

#. Create a new module containing your resolver function,
    e.g. in the ``resolver.py`` in any package/directory.

#. Set the ``DYNAMIC_HOST_RESOLVER_FUNC`` setting to the dotted Python
    import path of the module containing your resolver function

    .. code-block:: python

        DYNAMIC_HOST_RESOLVER_FUNC = 'path.to.resolver'

#. Set the ``DYNAMIC_HOST_RESOLVER_FUNC`` setting to the **PATH** of the above function

.. _`repository on Github`: https://github.com/goodnewsj62/django-dynamic-host

Configurations
------------------------------------------------------
**DYNAMIC_HOST_DEFAULT_HOSTS:**
To add a number of host manually(like you do with ALLOWED_HOST): Assign the list of default allowed hosts to ``DYNAMIC_HOST_DEFAULT_HOSTS`` in your settings.py.  
**Note:** This does not stop host not listed in DYNAMIC_HOST_DEFAULT_HOSTS from be validated via the resolver_func. Once django dynamic host  finds the incoming host in this list it just allows it and doesn't go future in calling the resolver_func.

**DYNAMIC_HOST_ALLOW_ALL:**
Although it is not recommended to open up to all host, but in some test cases or during development you may want to do so. Setting ``DYNAMIC_HOST_ALLOW_ALL`` to **True** opens your backend to all hosts

**DYNAMIC_HOST_ALLOW_SITES:**
Settings this value to True makes django dynamic host aware of you adding contrib.sites to your installed app. that way sites created via the sites model is automatically allowed.

**DYNAMIC_HOST_RESOLVER_FUNC:**
This holds the string path to your resolver function. this function should return a boolean value. If value is True then the domain is allowed else it is disallowed.


NOTE
------------------------------------------------------------------------
When django ``DEBUG=True`` there is no need to manually add localhost or 127.0.0.1 as they are automatically added and allowed under the hood.


**AllowedHostMiddleWare SHOULD ALWAYS SIT AT THE TOP AS IT'S JOB IS TO FIRST OF ALL VALIDATE IF AN INCOMING REQUEST FROM A HOST SHOULD BE ALLOWED TO GAIN ACCESS TO RESOURCE**