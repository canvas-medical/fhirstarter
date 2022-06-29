# Technical Design Details and Rationale

The approach taken by FHIRStarter to define API routes is somewhat novel. Typically, API routes are
created in FastAPI by using decorators on functions that implement the API routes. However, because
the FHIR standard specifies exactly what API routes should look like, is it not necessary for, and
would potentially introduce inconsistency, if developers defined API routes.

To enforce the methodology of API route creation, FHIRStarter instead asks the developer to provide
a callable with a recognizable function signature, and then decorate it with a FHIRStarter decorator
to register and designate it as a FHIR interaction. FHIRStarter takes care of the rest.

Developers are not precluded from adding API routes in the typical way with FastAPI decorators,
however this should be done only when needed.

The features that FHIRStarter provides are:

* Automatic, standardized API route creation
* Automatically generated capability statement and capability statement API route
* An exception-handling framework that produces FHIR-friendly responses (i.e. OperationOutcomes)
* Automatically generated, integrated documentation generated from the FHIR specification.

The most novel aspect of FHIRStarter is that dynamically creates the functions that implement API
routes. It accomplishes this by using the Python type FunctionType. Creation of a FunctionType
produces a callable that can be used like any Python callable, and these callables can be passed to
FastAPI during API route creation.

The data required to create a FunctionType are the following:

* A code object
* A dictionary of globals, which define all external symbols in the function template
* A tuple of argument defaults
* Type annotations for function arguments

The code object is obtained from the function templates defined in this package. These code objects
are simple functions that just pass through the request to another callable: the callable that the
developer decorates when registering a FHIR interaction.

The globals dictionary provides the context needed for the callable to run. This dictionary defines
the symbols referenced by the code of the callable. If globals are not defined, then the symbols the
code object references will be undefined.

The argument defaults and type annotations must be defined correctly for FastAPI API route creation
and documentation generation to work properly.0

FastAPI generates API routes and API documentation based on the list of function arguments, the type
annotations, and default arguments. If a FunctionType is properly created using the data listed
above then it is suitable to be passed to FastAPI as a callable.
