# Technical Design Details and Rationale

FHIRStarter implements a provider-decorator pattern on top of the FastAPI framework and FHIR
Resources Pydantic models. Typically, API routes are created in FastAPI by using decorators on
functions that implement the API routes. However, because the FHIR standard specifies exactly what
API routes should look like, is it not necessary for, and might potentially introduce inconsistency,
if developers defined API routes.

To enforce the methodology of API route creation, FHIRStarter instead asks the developer to provide
a handler with a recognizable function signature, and then decorate it with a FHIRStarter decorator
to register and designate it as a FHIR interaction. FHIRStarter takes care of the rest.

Developers are not precluded from adding API routes in the typical way with FastAPI decorators,
however this should be done only when needed.

FHIRStarter wraps the developer-provided handler using some simple functional programming techniques
and other features of Python in order to produce a callable that can be passed to FastAPI during API
route creation.

Particular attention should be paid to function signatures -- specifically variable names,
annotations, and defaults -- because FastAPI uses this information for documentation generation.
Annotations are overridden in several cases to ensure that the correct types are used for
documentation generation, and in the search use case, the function signature itself must be changed.

The resultant wrapper functions have signatures that adhere to the FHIR specification, and they
forward the requests on to the handlers provided by the developer.

# Contributions

If you would like to contribute to FHIRStarter, consider discussing your contribution on GitHub, 
or simply fork the project and submit a pull request.
