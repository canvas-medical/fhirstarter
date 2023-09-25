"""Expected OpenAPI schema for OpenAPI tests"""

EXPECTED_SCHEMA = {
    "openapi": "3.1.0",
    "info": {"title": "FHIRStarter", "version": "0.1.0"},
    "paths": {
        "/metadata": {
            "get": {
                "tags": ["System"],
                "summary": "capabilities",
                "description": "The capabilities interaction retrieves the information about a server's capabilities - which portions of the FHIR specification it supports.",
                "operationId": "fhirstarter|system|capabilities|get",
                "parameters": [
                    {
                        "description": "Override the HTTP content negotiation to specify JSON or XML response format",
                        "required": False,
                        "schema": {
                            "type": "string",
                            "title": " Format",
                            "description": "Override the HTTP content negotiation to specify JSON or XML response format",
                        },
                        "name": "_format",
                        "in": "query",
                    },
                    {
                        "description": "Ask for a pretty printed response for human convenience",
                        "required": False,
                        "schema": {
                            "type": "string",
                            "title": " Pretty",
                            "description": "Ask for a pretty printed response for human convenience",
                        },
                        "name": "_pretty",
                        "in": "query",
                    },
                ],
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/fhir+json": {
                                "schema": {
                                    "$ref": "#/components/schemas/CapabilityStatement"
                                },
                                "examples": {
                                    "example": {
                                        "summary": "General Capability Example",
                                        "description": "General Capability Example",
                                        "value": {
                                            "resourceType": "CapabilityStatement",
                                            "id": "example",
                                            "text": {
                                                "status": "generated",
                                                "div": '<div xmlns="http://www.w3.org/1999/xhtml">\n\t\t\t\n      <p>The EHR Server supports the following transactions for the resource Person: read, vread, \n        update, history, search(name,gender), create and updates.</p>\n\t\t\t\n      <p>The EHR System supports the following message: admin-notify::Person.</p>\n\t\t\t\n      <p>The EHR Application has a \n        \n        <a href="http://fhir.hl7.org/base/Profilebc054d23-75e1-4dc6-aca5-838b6b1ac81d/_history/b5fdd9fc-b021-4ea1-911a-721a60663796">general document profile</a>.\n      \n      </p>\n\t\t\n    </div>',
                                            },
                                            "url": "urn:uuid:68d043b5-9ecf-4559-a57a-396e0d452311",
                                            "version": "20130510",
                                            "name": "ACMEEHR",
                                            "title": "ACME EHR capability statement",
                                            "status": "draft",
                                            "experimental": True,
                                            "date": "2012-01-04",
                                            "publisher": "ACME Corporation",
                                            "contact": [
                                                {
                                                    "name": "System Administrator",
                                                    "telecom": [
                                                        {
                                                            "system": "email",
                                                            "value": "wile@acme.org",
                                                        }
                                                    ],
                                                }
                                            ],
                                            "description": "This is the FHIR capability statement for the main EHR at ACME for the private interface - it does not describe the public interface",
                                            "useContext": [
                                                {
                                                    "code": {
                                                        "system": "http://terminology.hl7.org/CodeSystem/usage-context-type",
                                                        "code": "focus",
                                                    },
                                                    "valueCodeableConcept": {
                                                        "coding": [
                                                            {
                                                                "system": "http://terminology.hl7.org/CodeSystem/variant-state",
                                                                "code": "positive",
                                                            }
                                                        ]
                                                    },
                                                }
                                            ],
                                            "jurisdiction": [
                                                {
                                                    "coding": [
                                                        {
                                                            "system": "urn:iso:std:iso:3166",
                                                            "code": "US",
                                                            "display": "United States of America (the)",
                                                        }
                                                    ]
                                                }
                                            ],
                                            "purpose": "Main EHR capability statement, published for contracting and operational support",
                                            "copyright": "Copyright © Acme Healthcare and GoodCorp EHR Systems",
                                            "kind": "instance",
                                            "instantiates": [
                                                "http://ihe.org/fhir/CapabilityStatement/pixm-client"
                                            ],
                                            "software": {
                                                "name": "EHR",
                                                "version": "0.00.020.2134",
                                                "releaseDate": "2012-01-04",
                                            },
                                            "implementation": {
                                                "description": "main EHR at ACME",
                                                "url": "http://10.2.3.4/fhir",
                                            },
                                            "fhirVersion": "5.0.0",
                                            "format": ["xml", "json"],
                                            "patchFormat": [
                                                "application/xml-patch+xml",
                                                "application/json-patch+json",
                                            ],
                                            "acceptLanguage": ["en", "es"],
                                            "implementationGuide": [
                                                "http://example.org/fhir/us/lab"
                                            ],
                                            "rest": [
                                                {
                                                    "mode": "server",
                                                    "documentation": "Main FHIR endpoint for acem health",
                                                    "security": {
                                                        "cors": True,
                                                        "service": [
                                                            {
                                                                "coding": [
                                                                    {
                                                                        "system": "http://hl7.org/fhir/restful-security-service",
                                                                        "code": "SMART-on-FHIR",
                                                                    }
                                                                ]
                                                            }
                                                        ],
                                                        "description": "See Smart on FHIR documentation",
                                                    },
                                                    "resource": [
                                                        {
                                                            "type": "Patient",
                                                            "profile": "http://registry.fhir.org/r5/StructureDefinition/7896271d-57f6-4231-89dc-dcc91eab2416",
                                                            "supportedProfile": [
                                                                "http://registry.fhir.org/r5/StructureDefinition/00ab9e7a-06c7-4f77-9234-4154ca1e3347"
                                                            ],
                                                            "documentation": "This server does not let the clients create identities.",
                                                            "interaction": [
                                                                {"code": "read"},
                                                                {
                                                                    "code": "vread",
                                                                    "documentation": "Only supported for patient records since 12-Dec 2012",
                                                                },
                                                                {"code": "update"},
                                                                {
                                                                    "code": "history-instance"
                                                                },
                                                                {"code": "create"},
                                                                {
                                                                    "code": "history-type"
                                                                },
                                                            ],
                                                            "versioning": "versioned-update",
                                                            "readHistory": True,
                                                            "updateCreate": False,
                                                            "conditionalCreate": True,
                                                            "conditionalRead": "full-support",
                                                            "conditionalUpdate": False,
                                                            "conditionalPatch": False,
                                                            "conditionalDelete": "not-supported",
                                                            "searchInclude": [
                                                                "Patient:organization"
                                                            ],
                                                            "searchRevInclude": [
                                                                "Person:patient"
                                                            ],
                                                            "searchParam": [
                                                                {
                                                                    "name": "identifier",
                                                                    "definition": "http://hl7.org/fhir/SearchParameter/Patient-identifier",
                                                                    "type": "token",
                                                                    "documentation": "Only supports search by institution MRN",
                                                                },
                                                                {
                                                                    "name": "general-practitioner",
                                                                    "definition": "http://hl7.org/fhir/SearchParameter/Patient-general-practitioner",
                                                                    "type": "reference",
                                                                },
                                                            ],
                                                        }
                                                    ],
                                                    "interaction": [
                                                        {"code": "transaction"},
                                                        {"code": "history-system"},
                                                    ],
                                                    "compartment": [
                                                        "http://hl7.org/fhir/CompartmentDefinition/patient"
                                                    ],
                                                }
                                            ],
                                            "messaging": [
                                                {
                                                    "endpoint": [
                                                        {
                                                            "protocol": {
                                                                "system": "http://hl7.org/fhir/message-transport",
                                                                "code": "mllp",
                                                            },
                                                            "address": "mllp:10.1.1.10:9234",
                                                        }
                                                    ],
                                                    "reliableCache": 30,
                                                    "documentation": "ADT A08 equivalent for external system notifications",
                                                    "supportedMessage": [
                                                        {
                                                            "mode": "receiver",
                                                            "definition": "http://hl7.org/fhir/MessageDefinition/example",
                                                        }
                                                    ],
                                                }
                                            ],
                                            "document": [
                                                {
                                                    "mode": "consumer",
                                                    "documentation": "Basic rules for all documents in the EHR system",
                                                    "profile": "http://fhir.hl7.org/base/Profilebc054d23-75e1-4dc6-aca5-838b6b1ac81d/_history/b5fdd9fc-b021-4ea1-911a-721a60663796",
                                                }
                                            ],
                                        },
                                    },
                                    "phr": {
                                        "summary": "PHR Example",
                                        "description": "PHR Example",
                                        "externalValue": "https://hl7.org/fhir/R5/capabilitystatement-phr-example.json",
                                    },
                                    "capabilitystatement-base": {
                                        "summary": "Complete Capability Statement",
                                        "description": "Complete Capability Statement",
                                        "externalValue": "https://hl7.org/fhir/R5/capabilitystatement-base.json",
                                    },
                                    "capabilitystatement-base2": {
                                        "summary": "EmptyCapabilityStatement",
                                        "description": "EmptyCapabilityStatement",
                                        "externalValue": "https://hl7.org/fhir/R5/capabilitystatement-base2.json",
                                    },
                                    "example-terminology-server": {
                                        "summary": "Terminology Server Base Capability Statement",
                                        "description": "Terminology Server Base Capability Statement",
                                        "externalValue": "https://hl7.org/fhir/R5/capabilitystatement-terminology-server.json",
                                    },
                                    "knowledge-repository": {
                                        "summary": "Knowledge Repository Base Capability Statement",
                                        "description": "Knowledge Repository Base Capability Statement",
                                        "externalValue": "https://hl7.org/fhir/R5/capabilitystatement-knowledge-repository.json",
                                    },
                                    "measure-processor": {
                                        "summary": "Measure Processor Base Capability Statement",
                                        "description": "Measure Processor Base Capability Statement",
                                        "externalValue": "https://hl7.org/fhir/R5/capabilitystatement-measure-processor.json",
                                    },
                                    "messagedefinition": {
                                        "summary": "Showing new message definition structure",
                                        "description": "Showing new message definition structure",
                                        "externalValue": "https://hl7.org/fhir/R5/capabilitystatement-messagedefinition.json",
                                    },
                                },
                            }
                        },
                    }
                },
            }
        },
        "/Patient": {
            "get": {
                "tags": ["Type:Patient"],
                "summary": "Patient search-type",
                "description": "The Patient search-type interaction searches a set of resources based on some filter criteria.",
                "operationId": "fhirstarter|type|search-type|get|Patient|fhir.resources.patient|Patient",
                "parameters": [
                    {
                        "description": "A portion of the family name of the patient",
                        "required": False,
                        "schema": {
                            "type": "string",
                            "title": "Family",
                            "description": "A portion of the family name of the patient",
                        },
                        "name": "family",
                        "in": "query",
                    },
                    {
                        "description": "Patient's nominated general practitioner, not the organization that manages the record",
                        "required": False,
                        "schema": {
                            "type": "string",
                            "title": "General-Practitioner",
                            "description": "Patient's nominated general practitioner, not the organization that manages the record",
                        },
                        "name": "general-practitioner",
                        "in": "query",
                    },
                    {
                        "description": "Nickname",
                        "required": False,
                        "schema": {
                            "type": "string",
                            "title": "Nickname",
                            "description": "Nickname",
                        },
                        "name": "nickname",
                        "in": "query",
                    },
                    {
                        "description": "When the resource version last changed",
                        "required": False,
                        "schema": {
                            "type": "string",
                            "title": " Lastupdated",
                            "description": "When the resource version last changed",
                        },
                        "name": "_lastUpdated",
                        "in": "query",
                    },
                    {
                        "description": "Override the HTTP content negotiation to specify JSON or XML response format",
                        "required": False,
                        "schema": {
                            "type": "string",
                            "title": " Format",
                            "description": "Override the HTTP content negotiation to specify JSON or XML response format",
                        },
                        "name": "_format",
                        "in": "query",
                    },
                    {
                        "description": "Ask for a pretty printed response for human convenience",
                        "required": False,
                        "schema": {
                            "type": "string",
                            "title": " Pretty",
                            "description": "Ask for a pretty printed response for human convenience",
                        },
                        "name": "_pretty",
                        "in": "query",
                    },
                ],
                "responses": {
                    "200": {
                        "description": "Successful Patient search-type",
                        "content": {
                            "application/fhir+json": {
                                "schema": {"$ref": "#/components/schemas/Bundle"},
                                "example": {
                                    "resourceType": "Bundle",
                                    "id": "bundle-example",
                                    "meta": {"lastUpdated": "2014-08-18T01:43:30Z"},
                                    "type": "searchset",
                                    "total": 3,
                                    "link": [
                                        {
                                            "relation": "self",
                                            "url": "https://example.com/base/Patient?_count=1",
                                        },
                                        {
                                            "relation": "next",
                                            "url": "https://example.com/base/Patient?searchId=ff15fd40-ff71-4b48-b366-09c706bed9d0&page=2",
                                        },
                                    ],
                                    "entry": [
                                        {
                                            "fullUrl": "https://example.com/base/Patient/example",
                                            "resource": {
                                                "resourceType": "Patient",
                                                "id": "example",
                                                "text": {
                                                    "status": "generated",
                                                    "div": '<div xmlns="http://www.w3.org/1999/xhtml"><p style="border: 1px #661aff solid; background-color: #e6e6ff; padding: 10px;"><b>Jim </b> male, DoB: 1974-12-25 ( Medical record number: 12345\xa0(use:\xa0USUAL,\xa0period:\xa02001-05-06 --&gt; (ongoing)))</p><hr/><table class="grid"><tr><td style="background-color: #f3f5da" title="Record is active">Active:</td><td>true</td><td style="background-color: #f3f5da" title="Known status of Patient">Deceased:</td><td colspan="3">false</td></tr><tr><td style="background-color: #f3f5da" title="Alternate names (see the one above)">Alt Names:</td><td colspan="3"><ul><li>Peter James Chalmers (OFFICIAL)</li><li>Peter James Windsor (MAIDEN)</li></ul></td></tr><tr><td style="background-color: #f3f5da" title="Ways to contact the Patient">Contact Details:</td><td colspan="3"><ul><li>-unknown-(HOME)</li><li>ph: (03) 5555 6473(WORK)</li><li>ph: (03) 3410 5613(MOBILE)</li><li>ph: (03) 5555 8834(OLD)</li><li>534 Erewhon St PeasantVille, Rainbow, Vic  3999(HOME)</li></ul></td></tr><tr><td style="background-color: #f3f5da" title="Nominated Contact: Next-of-Kin">Next-of-Kin:</td><td colspan="3"><ul><li>Bénédicte du Marché  (female)</li><li>534 Erewhon St PleasantVille Vic 3999 (HOME)</li><li><a href="tel:+33(237)998327">+33 (237) 998327</a></li><li>Valid Period: 2012 --&gt; (ongoing)</li></ul></td></tr><tr><td style="background-color: #f3f5da" title="Patient Links">Links:</td><td colspan="3"><ul><li>Managing Organization: <a href="organization-example-gastro.html">Organization/1</a> &quot;Gastroenterology&quot;</li></ul></td></tr></table></div>',
                                                },
                                                "identifier": [
                                                    {
                                                        "use": "usual",
                                                        "type": {
                                                            "coding": [
                                                                {
                                                                    "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                                                                    "code": "MR",
                                                                }
                                                            ]
                                                        },
                                                        "system": "urn:oid:1.2.36.146.595.217.0.1",
                                                        "value": "12345",
                                                        "period": {
                                                            "start": "2001-05-06"
                                                        },
                                                        "assigner": {
                                                            "display": "Acme Healthcare"
                                                        },
                                                    }
                                                ],
                                                "active": True,
                                                "name": [
                                                    {
                                                        "use": "official",
                                                        "family": "Chalmers",
                                                        "given": ["Peter", "James"],
                                                    },
                                                    {"use": "usual", "given": ["Jim"]},
                                                    {
                                                        "use": "maiden",
                                                        "family": "Windsor",
                                                        "given": ["Peter", "James"],
                                                        "period": {"end": "2002"},
                                                    },
                                                ],
                                                "telecom": [
                                                    {"use": "home"},
                                                    {
                                                        "system": "phone",
                                                        "value": "(03) 5555 6473",
                                                        "use": "work",
                                                        "rank": 1,
                                                    },
                                                    {
                                                        "system": "phone",
                                                        "value": "(03) 3410 5613",
                                                        "use": "mobile",
                                                        "rank": 2,
                                                    },
                                                    {
                                                        "system": "phone",
                                                        "value": "(03) 5555 8834",
                                                        "use": "old",
                                                        "period": {"end": "2014"},
                                                    },
                                                ],
                                                "gender": "male",
                                                "birthDate": "1974-12-25",
                                                "_birthDate": {
                                                    "extension": [
                                                        {
                                                            "url": "http://hl7.org/fhir/StructureDefinition/patient-birthTime",
                                                            "valueDateTime": "1974-12-25T14:35:45-05:00",
                                                        }
                                                    ]
                                                },
                                                "deceasedBoolean": False,
                                                "address": [
                                                    {
                                                        "use": "home",
                                                        "type": "both",
                                                        "text": "534 Erewhon St PeasantVille, Rainbow, Vic  3999",
                                                        "line": ["534 Erewhon St"],
                                                        "city": "PleasantVille",
                                                        "district": "Rainbow",
                                                        "state": "Vic",
                                                        "postalCode": "3999",
                                                        "period": {
                                                            "start": "1974-12-25"
                                                        },
                                                    }
                                                ],
                                                "contact": [
                                                    {
                                                        "relationship": [
                                                            {
                                                                "coding": [
                                                                    {
                                                                        "system": "http://terminology.hl7.org/CodeSystem/v2-0131",
                                                                        "code": "N",
                                                                    }
                                                                ]
                                                            }
                                                        ],
                                                        "name": {
                                                            "family": "du Marché",
                                                            "_family": {
                                                                "extension": [
                                                                    {
                                                                        "url": "http://hl7.org/fhir/StructureDefinition/humanname-own-prefix",
                                                                        "valueString": "VV",
                                                                    }
                                                                ]
                                                            },
                                                            "given": ["Bénédicte"],
                                                        },
                                                        "telecom": [
                                                            {
                                                                "system": "phone",
                                                                "value": "+33 (237) 998327",
                                                            }
                                                        ],
                                                        "address": {
                                                            "use": "home",
                                                            "type": "both",
                                                            "line": ["534 Erewhon St"],
                                                            "city": "PleasantVille",
                                                            "district": "Rainbow",
                                                            "state": "Vic",
                                                            "postalCode": "3999",
                                                            "period": {
                                                                "start": "1974-12-25"
                                                            },
                                                        },
                                                        "gender": "female",
                                                        "period": {"start": "2012"},
                                                    }
                                                ],
                                                "managingOrganization": {
                                                    "reference": "Organization/1"
                                                },
                                            },
                                            "search": {"mode": "match", "score": 1},
                                        }
                                    ],
                                },
                            }
                        },
                    },
                    "400": {
                        "description": "Patient search-type request could not be parsed or failed basic FHIR validation rules.",
                        "content": {
                            "application/fhir+json": {
                                "schema": {
                                    "$ref": "#/components/schemas/OperationOutcome"
                                },
                                "example": {
                                    "resourceType": "OperationOutcome",
                                    "id": "101",
                                    "issue": [
                                        {
                                            "severity": "error",
                                            "code": "invalid",
                                            "details": {"text": "Bad request"},
                                        }
                                    ],
                                },
                            }
                        },
                    },
                    "401": {
                        "description": "Authentication is required for the Patient search-type interaction that was attempted.",
                        "content": {
                            "application/fhir+json": {
                                "schema": {
                                    "$ref": "#/components/schemas/OperationOutcome"
                                },
                                "example": {
                                    "resourceType": "OperationOutcome",
                                    "id": "101",
                                    "issue": [
                                        {
                                            "severity": "error",
                                            "code": "unknown",
                                            "details": {
                                                "text": "Authentication failed"
                                            },
                                        }
                                    ],
                                },
                            }
                        },
                    },
                    "403": {
                        "description": "Authorization is required for the Patient search-type interaction that was attempted.",
                        "content": {
                            "application/fhir+json": {
                                "schema": {
                                    "$ref": "#/components/schemas/OperationOutcome"
                                },
                                "example": {
                                    "resourceType": "OperationOutcome",
                                    "id": "101",
                                    "issue": [
                                        {
                                            "severity": "error",
                                            "code": "forbidden",
                                            "details": {"text": "Authorization failed"},
                                        }
                                    ],
                                },
                            }
                        },
                    },
                    "500": {
                        "description": "The server has encountered a situation it does not know how to handle.",
                        "content": {
                            "application/fhir+json": {
                                "schema": {
                                    "$ref": "#/components/schemas/OperationOutcome"
                                },
                                "example": {
                                    "resourceType": "OperationOutcome",
                                    "id": "101",
                                    "issue": [
                                        {
                                            "severity": "error",
                                            "code": "exception",
                                            "details": {
                                                "text": "Internal server error"
                                            },
                                        }
                                    ],
                                },
                            }
                        },
                    },
                },
            },
            "post": {
                "tags": ["Type:Patient"],
                "summary": "Patient create",
                "description": "The Patient create interaction creates a new Patient resource in a server-assigned location.",
                "operationId": "fhirstarter|type|create|post|Patient|fhir.resources.patient|Patient",
                "parameters": [
                    {
                        "description": "Override the HTTP content negotiation to specify JSON or XML response format",
                        "required": False,
                        "schema": {
                            "type": "string",
                            "title": " Format",
                            "description": "Override the HTTP content negotiation to specify JSON or XML response format",
                        },
                        "name": "_format",
                        "in": "query",
                    },
                    {
                        "description": "Ask for a pretty printed response for human convenience",
                        "required": False,
                        "schema": {
                            "type": "string",
                            "title": " Pretty",
                            "description": "Ask for a pretty printed response for human convenience",
                        },
                        "name": "_pretty",
                        "in": "query",
                    },
                ],
                "requestBody": {
                    "content": {
                        "application/fhir+json": {
                            "schema": {"$ref": "#/components/schemas/Patient"},
                            "examples": {
                                "example": {
                                    "summary": "General Person Example",
                                    "description": "General Person Example",
                                    "value": {
                                        "resourceType": "Patient",
                                        "id": "example",
                                        "text": {
                                            "status": "generated",
                                            "div": '<div xmlns="http://www.w3.org/1999/xhtml"><p style="border: 1px #661aff solid; background-color: #e6e6ff; padding: 10px;"><b>Jim </b> male, DoB: 1974-12-25 ( Medical record number: 12345\xa0(use:\xa0USUAL,\xa0period:\xa02001-05-06 --&gt; (ongoing)))</p><hr/><table class="grid"><tr><td style="background-color: #f3f5da" title="Record is active">Active:</td><td>true</td><td style="background-color: #f3f5da" title="Known status of Patient">Deceased:</td><td colspan="3">false</td></tr><tr><td style="background-color: #f3f5da" title="Alternate names (see the one above)">Alt Names:</td><td colspan="3"><ul><li>Peter James Chalmers (OFFICIAL)</li><li>Peter James Windsor (MAIDEN)</li></ul></td></tr><tr><td style="background-color: #f3f5da" title="Ways to contact the Patient">Contact Details:</td><td colspan="3"><ul><li>-unknown-(HOME)</li><li>ph: (03) 5555 6473(WORK)</li><li>ph: (03) 3410 5613(MOBILE)</li><li>ph: (03) 5555 8834(OLD)</li><li>534 Erewhon St PeasantVille, Rainbow, Vic  3999(HOME)</li></ul></td></tr><tr><td style="background-color: #f3f5da" title="Nominated Contact: Next-of-Kin">Next-of-Kin:</td><td colspan="3"><ul><li>Bénédicte du Marché  (female)</li><li>534 Erewhon St PleasantVille Vic 3999 (HOME)</li><li><a href="tel:+33(237)998327">+33 (237) 998327</a></li><li>Valid Period: 2012 --&gt; (ongoing)</li></ul></td></tr><tr><td style="background-color: #f3f5da" title="Patient Links">Links:</td><td colspan="3"><ul><li>Managing Organization: <a href="organization-example-gastro.html">Organization/1</a> &quot;Gastroenterology&quot;</li></ul></td></tr></table></div>',
                                        },
                                        "identifier": [
                                            {
                                                "use": "usual",
                                                "type": {
                                                    "coding": [
                                                        {
                                                            "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                                                            "code": "MR",
                                                        }
                                                    ]
                                                },
                                                "system": "urn:oid:1.2.36.146.595.217.0.1",
                                                "value": "12345",
                                                "period": {"start": "2001-05-06"},
                                                "assigner": {
                                                    "display": "Acme Healthcare"
                                                },
                                            }
                                        ],
                                        "active": True,
                                        "name": [
                                            {
                                                "use": "official",
                                                "family": "Chalmers",
                                                "given": ["Peter", "James"],
                                            },
                                            {"use": "usual", "given": ["Jim"]},
                                            {
                                                "use": "maiden",
                                                "family": "Windsor",
                                                "given": ["Peter", "James"],
                                                "period": {"end": "2002"},
                                            },
                                        ],
                                        "telecom": [
                                            {"use": "home"},
                                            {
                                                "system": "phone",
                                                "value": "(03) 5555 6473",
                                                "use": "work",
                                                "rank": 1,
                                            },
                                            {
                                                "system": "phone",
                                                "value": "(03) 3410 5613",
                                                "use": "mobile",
                                                "rank": 2,
                                            },
                                            {
                                                "system": "phone",
                                                "value": "(03) 5555 8834",
                                                "use": "old",
                                                "period": {"end": "2014"},
                                            },
                                        ],
                                        "gender": "male",
                                        "birthDate": "1974-12-25",
                                        "_birthDate": {
                                            "extension": [
                                                {
                                                    "url": "http://hl7.org/fhir/StructureDefinition/patient-birthTime",
                                                    "valueDateTime": "1974-12-25T14:35:45-05:00",
                                                }
                                            ]
                                        },
                                        "deceasedBoolean": False,
                                        "address": [
                                            {
                                                "use": "home",
                                                "type": "both",
                                                "text": "534 Erewhon St PeasantVille, Rainbow, Vic  3999",
                                                "line": ["534 Erewhon St"],
                                                "city": "PleasantVille",
                                                "district": "Rainbow",
                                                "state": "Vic",
                                                "postalCode": "3999",
                                                "period": {"start": "1974-12-25"},
                                            }
                                        ],
                                        "contact": [
                                            {
                                                "relationship": [
                                                    {
                                                        "coding": [
                                                            {
                                                                "system": "http://terminology.hl7.org/CodeSystem/v2-0131",
                                                                "code": "N",
                                                            }
                                                        ]
                                                    }
                                                ],
                                                "name": {
                                                    "family": "du Marché",
                                                    "_family": {
                                                        "extension": [
                                                            {
                                                                "url": "http://hl7.org/fhir/StructureDefinition/humanname-own-prefix",
                                                                "valueString": "VV",
                                                            }
                                                        ]
                                                    },
                                                    "given": ["Bénédicte"],
                                                },
                                                "telecom": [
                                                    {
                                                        "system": "phone",
                                                        "value": "+33 (237) 998327",
                                                    }
                                                ],
                                                "address": {
                                                    "use": "home",
                                                    "type": "both",
                                                    "line": ["534 Erewhon St"],
                                                    "city": "PleasantVille",
                                                    "district": "Rainbow",
                                                    "state": "Vic",
                                                    "postalCode": "3999",
                                                    "period": {"start": "1974-12-25"},
                                                },
                                                "gender": "female",
                                                "period": {"start": "2012"},
                                            }
                                        ],
                                        "managingOrganization": {
                                            "reference": "Organization/1"
                                        },
                                    },
                                },
                                "pat1": {
                                    "summary": "Patient 1 for linking",
                                    "description": "Patient 1 for linking",
                                    "externalValue": "https://hl7.org/fhir/R5/patient-example-a.json",
                                },
                                "pat2": {
                                    "summary": "Patient 2 for linking",
                                    "description": "Patient 2 for linking",
                                    "externalValue": "https://hl7.org/fhir/R5/patient-example-b.json",
                                },
                                "pat3": {
                                    "summary": "Deceased patient (using time)",
                                    "description": "Deceased patient (using time)",
                                    "externalValue": "https://hl7.org/fhir/R5/patient-example-c.json",
                                },
                                "pat4": {
                                    "summary": "Deceased patient (using boolean)",
                                    "description": "Deceased patient (using boolean)",
                                    "externalValue": "https://hl7.org/fhir/R5/patient-example-d.json",
                                },
                                "b248b1b2-1686-4b94-9936-37d7a5f94b51": {
                                    "summary": "Stock people (defined by HL7 publishing)",
                                    "description": "Stock people (defined by HL7 publishing)",
                                    "externalValue": "https://hl7.org/fhir/R5/patient-examples-general.json",
                                },
                                "patient-example-sex-and-gender": {
                                    "summary": "Transgender Person Example",
                                    "description": "Transgender Person Example",
                                    "externalValue": "https://hl7.org/fhir/R5/patient-example-sex-and-gender.json",
                                },
                                "b3f24cf14-d349-45b3-8134-3d83e9104875": {
                                    "summary": "Example People from cypress project",
                                    "description": "Example People from cypress project",
                                    "externalValue": "https://hl7.org/fhir/R5/patient-examples-cypress-template.json",
                                },
                                "xcda": {
                                    "summary": "2nd person example",
                                    "description": "2nd person example",
                                    "externalValue": "https://hl7.org/fhir/R5/patient-example-xcda.json",
                                },
                                "xds": {
                                    "summary": "XDS Patient",
                                    "description": "XDS Patient",
                                    "externalValue": "https://hl7.org/fhir/R5/patient-example-xds.json",
                                },
                                "animal": {
                                    "summary": "An example of an animal",
                                    "description": "An example of an animal",
                                    "externalValue": "https://hl7.org/fhir/R5/patient-example-animal.json",
                                },
                                "dicom": {
                                    "summary": "Taken from a DICOM sample",
                                    "description": "Taken from a DICOM sample",
                                    "externalValue": "https://hl7.org/fhir/R5/patient-example-dicom.json",
                                },
                                "ihe-pcd": {
                                    "summary": "Example from IHE-PCD example",
                                    "description": "Example from IHE-PCD example",
                                    "externalValue": "https://hl7.org/fhir/R5/patient-example-ihe-pcd.json",
                                },
                                "f001": {
                                    "summary": "Real-world patient example (anonymized)",
                                    "description": "Real-world patient example (anonymized)",
                                    "externalValue": "https://hl7.org/fhir/R5/patient-example-f001-pieter.json",
                                },
                                "f201": {
                                    "summary": "Real-world patient example (anonymized)",
                                    "description": "Real-world patient example (anonymized)",
                                    "externalValue": "https://hl7.org/fhir/R5/patient-example-f201-roel.json",
                                },
                                "glossy": {
                                    "summary": "Example for glossy",
                                    "description": "Example for glossy",
                                    "externalValue": "https://hl7.org/fhir/R5/patient-glossy-example.json",
                                },
                                "proband": {
                                    "summary": "Genetic Risk Assessment Person",
                                    "description": "Genetic Risk Assessment Person",
                                    "externalValue": "https://hl7.org/fhir/R5/patient-example-proband.json",
                                },
                                "genetics-example1": {
                                    "summary": "Additional Genetics Example",
                                    "description": "Additional Genetics Example",
                                    "externalValue": "https://hl7.org/fhir/R5/patient-genetics-example1.json",
                                },
                                "ch-example": {
                                    "summary": "Example Patient resource with Chinese content",
                                    "description": "Example Patient resource with Chinese content",
                                    "externalValue": "https://hl7.org/fhir/R5/patient-example-chinese.json",
                                },
                                "newborn": {
                                    "summary": "Newborn Patient Example",
                                    "description": "Newborn Patient Example",
                                    "externalValue": "https://hl7.org/fhir/R5/patient-example-newborn.json",
                                },
                                "mom": {
                                    "summary": "Mother of Newborn Patient Example",
                                    "description": "Mother of Newborn Patient Example",
                                    "externalValue": "https://hl7.org/fhir/R5/patient-example-mom.json",
                                },
                                "infant-twin-1": {
                                    "summary": "Newborn Eldest Twin Example",
                                    "description": "Newborn Eldest Twin Example",
                                    "externalValue": "https://hl7.org/fhir/R5/patient-example-infant-twin-1.json",
                                },
                                "infant-twin-2": {
                                    "summary": "Newborn Youngest Twin Example",
                                    "description": "Newborn Youngest Twin Example",
                                    "externalValue": "https://hl7.org/fhir/R5/patient-example-infant-twin-2.json",
                                },
                                "infant-fetal": {
                                    "summary": "Pre-birth fetal infant Example",
                                    "description": "Pre-birth fetal infant Example",
                                    "externalValue": "https://hl7.org/fhir/R5/patient-example-infant-fetal.json",
                                },
                                "infant-mom": {
                                    "summary": "Mother of infant twins and fetal infant.",
                                    "description": "Mother of infant twins and fetal infant.",
                                    "externalValue": "https://hl7.org/fhir/R5/patient-example-infant-mom.json",
                                },
                            },
                        }
                    },
                    "required": True,
                },
                "responses": {
                    "201": {
                        "description": "Successful Patient create",
                        "content": {
                            "application/fhir+json": {
                                "schema": {"$ref": "#/components/schemas/Patient"},
                                "examples": {
                                    "example": {
                                        "summary": "General Person Example",
                                        "description": "General Person Example",
                                        "value": {
                                            "resourceType": "Patient",
                                            "id": "example",
                                            "text": {
                                                "status": "generated",
                                                "div": '<div xmlns="http://www.w3.org/1999/xhtml"><p style="border: 1px #661aff solid; background-color: #e6e6ff; padding: 10px;"><b>Jim </b> male, DoB: 1974-12-25 ( Medical record number: 12345\xa0(use:\xa0USUAL,\xa0period:\xa02001-05-06 --&gt; (ongoing)))</p><hr/><table class="grid"><tr><td style="background-color: #f3f5da" title="Record is active">Active:</td><td>true</td><td style="background-color: #f3f5da" title="Known status of Patient">Deceased:</td><td colspan="3">false</td></tr><tr><td style="background-color: #f3f5da" title="Alternate names (see the one above)">Alt Names:</td><td colspan="3"><ul><li>Peter James Chalmers (OFFICIAL)</li><li>Peter James Windsor (MAIDEN)</li></ul></td></tr><tr><td style="background-color: #f3f5da" title="Ways to contact the Patient">Contact Details:</td><td colspan="3"><ul><li>-unknown-(HOME)</li><li>ph: (03) 5555 6473(WORK)</li><li>ph: (03) 3410 5613(MOBILE)</li><li>ph: (03) 5555 8834(OLD)</li><li>534 Erewhon St PeasantVille, Rainbow, Vic  3999(HOME)</li></ul></td></tr><tr><td style="background-color: #f3f5da" title="Nominated Contact: Next-of-Kin">Next-of-Kin:</td><td colspan="3"><ul><li>Bénédicte du Marché  (female)</li><li>534 Erewhon St PleasantVille Vic 3999 (HOME)</li><li><a href="tel:+33(237)998327">+33 (237) 998327</a></li><li>Valid Period: 2012 --&gt; (ongoing)</li></ul></td></tr><tr><td style="background-color: #f3f5da" title="Patient Links">Links:</td><td colspan="3"><ul><li>Managing Organization: <a href="organization-example-gastro.html">Organization/1</a> &quot;Gastroenterology&quot;</li></ul></td></tr></table></div>',
                                            },
                                            "identifier": [
                                                {
                                                    "use": "usual",
                                                    "type": {
                                                        "coding": [
                                                            {
                                                                "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                                                                "code": "MR",
                                                            }
                                                        ]
                                                    },
                                                    "system": "urn:oid:1.2.36.146.595.217.0.1",
                                                    "value": "12345",
                                                    "period": {"start": "2001-05-06"},
                                                    "assigner": {
                                                        "display": "Acme Healthcare"
                                                    },
                                                }
                                            ],
                                            "active": True,
                                            "name": [
                                                {
                                                    "use": "official",
                                                    "family": "Chalmers",
                                                    "given": ["Peter", "James"],
                                                },
                                                {"use": "usual", "given": ["Jim"]},
                                                {
                                                    "use": "maiden",
                                                    "family": "Windsor",
                                                    "given": ["Peter", "James"],
                                                    "period": {"end": "2002"},
                                                },
                                            ],
                                            "telecom": [
                                                {"use": "home"},
                                                {
                                                    "system": "phone",
                                                    "value": "(03) 5555 6473",
                                                    "use": "work",
                                                    "rank": 1,
                                                },
                                                {
                                                    "system": "phone",
                                                    "value": "(03) 3410 5613",
                                                    "use": "mobile",
                                                    "rank": 2,
                                                },
                                                {
                                                    "system": "phone",
                                                    "value": "(03) 5555 8834",
                                                    "use": "old",
                                                    "period": {"end": "2014"},
                                                },
                                            ],
                                            "gender": "male",
                                            "birthDate": "1974-12-25",
                                            "_birthDate": {
                                                "extension": [
                                                    {
                                                        "url": "http://hl7.org/fhir/StructureDefinition/patient-birthTime",
                                                        "valueDateTime": "1974-12-25T14:35:45-05:00",
                                                    }
                                                ]
                                            },
                                            "deceasedBoolean": False,
                                            "address": [
                                                {
                                                    "use": "home",
                                                    "type": "both",
                                                    "text": "534 Erewhon St PeasantVille, Rainbow, Vic  3999",
                                                    "line": ["534 Erewhon St"],
                                                    "city": "PleasantVille",
                                                    "district": "Rainbow",
                                                    "state": "Vic",
                                                    "postalCode": "3999",
                                                    "period": {"start": "1974-12-25"},
                                                }
                                            ],
                                            "contact": [
                                                {
                                                    "relationship": [
                                                        {
                                                            "coding": [
                                                                {
                                                                    "system": "http://terminology.hl7.org/CodeSystem/v2-0131",
                                                                    "code": "N",
                                                                }
                                                            ]
                                                        }
                                                    ],
                                                    "name": {
                                                        "family": "du Marché",
                                                        "_family": {
                                                            "extension": [
                                                                {
                                                                    "url": "http://hl7.org/fhir/StructureDefinition/humanname-own-prefix",
                                                                    "valueString": "VV",
                                                                }
                                                            ]
                                                        },
                                                        "given": ["Bénédicte"],
                                                    },
                                                    "telecom": [
                                                        {
                                                            "system": "phone",
                                                            "value": "+33 (237) 998327",
                                                        }
                                                    ],
                                                    "address": {
                                                        "use": "home",
                                                        "type": "both",
                                                        "line": ["534 Erewhon St"],
                                                        "city": "PleasantVille",
                                                        "district": "Rainbow",
                                                        "state": "Vic",
                                                        "postalCode": "3999",
                                                        "period": {
                                                            "start": "1974-12-25"
                                                        },
                                                    },
                                                    "gender": "female",
                                                    "period": {"start": "2012"},
                                                }
                                            ],
                                            "managingOrganization": {
                                                "reference": "Organization/1"
                                            },
                                        },
                                    },
                                    "pat1": {
                                        "summary": "Patient 1 for linking",
                                        "description": "Patient 1 for linking",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-a.json",
                                    },
                                    "pat2": {
                                        "summary": "Patient 2 for linking",
                                        "description": "Patient 2 for linking",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-b.json",
                                    },
                                    "pat3": {
                                        "summary": "Deceased patient (using time)",
                                        "description": "Deceased patient (using time)",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-c.json",
                                    },
                                    "pat4": {
                                        "summary": "Deceased patient (using boolean)",
                                        "description": "Deceased patient (using boolean)",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-d.json",
                                    },
                                    "b248b1b2-1686-4b94-9936-37d7a5f94b51": {
                                        "summary": "Stock people (defined by HL7 publishing)",
                                        "description": "Stock people (defined by HL7 publishing)",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-examples-general.json",
                                    },
                                    "patient-example-sex-and-gender": {
                                        "summary": "Transgender Person Example",
                                        "description": "Transgender Person Example",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-sex-and-gender.json",
                                    },
                                    "b3f24cf14-d349-45b3-8134-3d83e9104875": {
                                        "summary": "Example People from cypress project",
                                        "description": "Example People from cypress project",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-examples-cypress-template.json",
                                    },
                                    "xcda": {
                                        "summary": "2nd person example",
                                        "description": "2nd person example",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-xcda.json",
                                    },
                                    "xds": {
                                        "summary": "XDS Patient",
                                        "description": "XDS Patient",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-xds.json",
                                    },
                                    "animal": {
                                        "summary": "An example of an animal",
                                        "description": "An example of an animal",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-animal.json",
                                    },
                                    "dicom": {
                                        "summary": "Taken from a DICOM sample",
                                        "description": "Taken from a DICOM sample",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-dicom.json",
                                    },
                                    "ihe-pcd": {
                                        "summary": "Example from IHE-PCD example",
                                        "description": "Example from IHE-PCD example",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-ihe-pcd.json",
                                    },
                                    "f001": {
                                        "summary": "Real-world patient example (anonymized)",
                                        "description": "Real-world patient example (anonymized)",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-f001-pieter.json",
                                    },
                                    "f201": {
                                        "summary": "Real-world patient example (anonymized)",
                                        "description": "Real-world patient example (anonymized)",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-f201-roel.json",
                                    },
                                    "glossy": {
                                        "summary": "Example for glossy",
                                        "description": "Example for glossy",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-glossy-example.json",
                                    },
                                    "proband": {
                                        "summary": "Genetic Risk Assessment Person",
                                        "description": "Genetic Risk Assessment Person",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-proband.json",
                                    },
                                    "genetics-example1": {
                                        "summary": "Additional Genetics Example",
                                        "description": "Additional Genetics Example",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-genetics-example1.json",
                                    },
                                    "ch-example": {
                                        "summary": "Example Patient resource with Chinese content",
                                        "description": "Example Patient resource with Chinese content",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-chinese.json",
                                    },
                                    "newborn": {
                                        "summary": "Newborn Patient Example",
                                        "description": "Newborn Patient Example",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-newborn.json",
                                    },
                                    "mom": {
                                        "summary": "Mother of Newborn Patient Example",
                                        "description": "Mother of Newborn Patient Example",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-mom.json",
                                    },
                                    "infant-twin-1": {
                                        "summary": "Newborn Eldest Twin Example",
                                        "description": "Newborn Eldest Twin Example",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-infant-twin-1.json",
                                    },
                                    "infant-twin-2": {
                                        "summary": "Newborn Youngest Twin Example",
                                        "description": "Newborn Youngest Twin Example",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-infant-twin-2.json",
                                    },
                                    "infant-fetal": {
                                        "summary": "Pre-birth fetal infant Example",
                                        "description": "Pre-birth fetal infant Example",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-infant-fetal.json",
                                    },
                                    "infant-mom": {
                                        "summary": "Mother of infant twins and fetal infant.",
                                        "description": "Mother of infant twins and fetal infant.",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-infant-mom.json",
                                    },
                                },
                            }
                        },
                    },
                    "400": {
                        "description": "Patient create request could not be parsed or failed basic FHIR validation rules.",
                        "content": {
                            "application/fhir+json": {
                                "schema": {
                                    "$ref": "#/components/schemas/OperationOutcome"
                                },
                                "example": {
                                    "resourceType": "OperationOutcome",
                                    "id": "101",
                                    "issue": [
                                        {
                                            "severity": "error",
                                            "code": "invalid",
                                            "details": {"text": "Bad request"},
                                        }
                                    ],
                                },
                            }
                        },
                    },
                    "401": {
                        "description": "Authentication is required for the Patient create interaction that was attempted.",
                        "content": {
                            "application/fhir+json": {
                                "schema": {
                                    "$ref": "#/components/schemas/OperationOutcome"
                                },
                                "example": {
                                    "resourceType": "OperationOutcome",
                                    "id": "101",
                                    "issue": [
                                        {
                                            "severity": "error",
                                            "code": "unknown",
                                            "details": {
                                                "text": "Authentication failed"
                                            },
                                        }
                                    ],
                                },
                            }
                        },
                    },
                    "403": {
                        "description": "Authorization is required for the Patient create interaction that was attempted.",
                        "content": {
                            "application/fhir+json": {
                                "schema": {
                                    "$ref": "#/components/schemas/OperationOutcome"
                                },
                                "example": {
                                    "resourceType": "OperationOutcome",
                                    "id": "101",
                                    "issue": [
                                        {
                                            "severity": "error",
                                            "code": "forbidden",
                                            "details": {"text": "Authorization failed"},
                                        }
                                    ],
                                },
                            }
                        },
                    },
                    "422": {
                        "description": "The proposed Patient resource violated applicable FHIR profiles or server business rules.",
                        "content": {
                            "application/fhir+json": {
                                "schema": {
                                    "$ref": "#/components/schemas/OperationOutcome"
                                },
                                "example": {
                                    "resourceType": "OperationOutcome",
                                    "id": "101",
                                    "issue": [
                                        {
                                            "severity": "error",
                                            "code": "processing",
                                            "details": {"text": "Unprocessable entity"},
                                        }
                                    ],
                                },
                            }
                        },
                    },
                    "500": {
                        "description": "The server has encountered a situation it does not know how to handle.",
                        "content": {
                            "application/fhir+json": {
                                "schema": {
                                    "$ref": "#/components/schemas/OperationOutcome"
                                },
                                "example": {
                                    "resourceType": "OperationOutcome",
                                    "id": "101",
                                    "issue": [
                                        {
                                            "severity": "error",
                                            "code": "exception",
                                            "details": {
                                                "text": "Internal server error"
                                            },
                                        }
                                    ],
                                },
                            }
                        },
                    },
                },
            },
        },
        "/Patient/{id}": {
            "get": {
                "tags": ["Type:Patient"],
                "summary": "Patient read",
                "description": "The Patient read interaction accesses the current contents of a Patient resource.",
                "operationId": "fhirstarter|instance|read|get|Patient|fhir.resources.patient|Patient",
                "parameters": [
                    {
                        "description": "Logical id of this artifact",
                        "required": True,
                        "schema": {
                            "type": "string",
                            "maxLength": 64,
                            "minLength": 1,
                            "pattern": "^[A-Za-z0-9\\-.]+$",
                            "title": "Id",
                            "description": "Logical id of this artifact",
                        },
                        "name": "id",
                        "in": "path",
                    },
                    {
                        "description": "Override the HTTP content negotiation to specify JSON or XML response format",
                        "required": False,
                        "schema": {
                            "type": "string",
                            "title": " Format",
                            "description": "Override the HTTP content negotiation to specify JSON or XML response format",
                        },
                        "name": "_format",
                        "in": "query",
                    },
                    {
                        "description": "Ask for a pretty printed response for human convenience",
                        "required": False,
                        "schema": {
                            "type": "string",
                            "title": " Pretty",
                            "description": "Ask for a pretty printed response for human convenience",
                        },
                        "name": "_pretty",
                        "in": "query",
                    },
                ],
                "responses": {
                    "200": {
                        "description": "Successful Patient read",
                        "content": {
                            "application/fhir+json": {
                                "schema": {"$ref": "#/components/schemas/Patient"},
                                "examples": {
                                    "example": {
                                        "summary": "General Person Example",
                                        "description": "General Person Example",
                                        "value": {
                                            "resourceType": "Patient",
                                            "id": "example",
                                            "text": {
                                                "status": "generated",
                                                "div": '<div xmlns="http://www.w3.org/1999/xhtml"><p style="border: 1px #661aff solid; background-color: #e6e6ff; padding: 10px;"><b>Jim </b> male, DoB: 1974-12-25 ( Medical record number: 12345\xa0(use:\xa0USUAL,\xa0period:\xa02001-05-06 --&gt; (ongoing)))</p><hr/><table class="grid"><tr><td style="background-color: #f3f5da" title="Record is active">Active:</td><td>true</td><td style="background-color: #f3f5da" title="Known status of Patient">Deceased:</td><td colspan="3">false</td></tr><tr><td style="background-color: #f3f5da" title="Alternate names (see the one above)">Alt Names:</td><td colspan="3"><ul><li>Peter James Chalmers (OFFICIAL)</li><li>Peter James Windsor (MAIDEN)</li></ul></td></tr><tr><td style="background-color: #f3f5da" title="Ways to contact the Patient">Contact Details:</td><td colspan="3"><ul><li>-unknown-(HOME)</li><li>ph: (03) 5555 6473(WORK)</li><li>ph: (03) 3410 5613(MOBILE)</li><li>ph: (03) 5555 8834(OLD)</li><li>534 Erewhon St PeasantVille, Rainbow, Vic  3999(HOME)</li></ul></td></tr><tr><td style="background-color: #f3f5da" title="Nominated Contact: Next-of-Kin">Next-of-Kin:</td><td colspan="3"><ul><li>Bénédicte du Marché  (female)</li><li>534 Erewhon St PleasantVille Vic 3999 (HOME)</li><li><a href="tel:+33(237)998327">+33 (237) 998327</a></li><li>Valid Period: 2012 --&gt; (ongoing)</li></ul></td></tr><tr><td style="background-color: #f3f5da" title="Patient Links">Links:</td><td colspan="3"><ul><li>Managing Organization: <a href="organization-example-gastro.html">Organization/1</a> &quot;Gastroenterology&quot;</li></ul></td></tr></table></div>',
                                            },
                                            "identifier": [
                                                {
                                                    "use": "usual",
                                                    "type": {
                                                        "coding": [
                                                            {
                                                                "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                                                                "code": "MR",
                                                            }
                                                        ]
                                                    },
                                                    "system": "urn:oid:1.2.36.146.595.217.0.1",
                                                    "value": "12345",
                                                    "period": {"start": "2001-05-06"},
                                                    "assigner": {
                                                        "display": "Acme Healthcare"
                                                    },
                                                }
                                            ],
                                            "active": True,
                                            "name": [
                                                {
                                                    "use": "official",
                                                    "family": "Chalmers",
                                                    "given": ["Peter", "James"],
                                                },
                                                {"use": "usual", "given": ["Jim"]},
                                                {
                                                    "use": "maiden",
                                                    "family": "Windsor",
                                                    "given": ["Peter", "James"],
                                                    "period": {"end": "2002"},
                                                },
                                            ],
                                            "telecom": [
                                                {"use": "home"},
                                                {
                                                    "system": "phone",
                                                    "value": "(03) 5555 6473",
                                                    "use": "work",
                                                    "rank": 1,
                                                },
                                                {
                                                    "system": "phone",
                                                    "value": "(03) 3410 5613",
                                                    "use": "mobile",
                                                    "rank": 2,
                                                },
                                                {
                                                    "system": "phone",
                                                    "value": "(03) 5555 8834",
                                                    "use": "old",
                                                    "period": {"end": "2014"},
                                                },
                                            ],
                                            "gender": "male",
                                            "birthDate": "1974-12-25",
                                            "_birthDate": {
                                                "extension": [
                                                    {
                                                        "url": "http://hl7.org/fhir/StructureDefinition/patient-birthTime",
                                                        "valueDateTime": "1974-12-25T14:35:45-05:00",
                                                    }
                                                ]
                                            },
                                            "deceasedBoolean": False,
                                            "address": [
                                                {
                                                    "use": "home",
                                                    "type": "both",
                                                    "text": "534 Erewhon St PeasantVille, Rainbow, Vic  3999",
                                                    "line": ["534 Erewhon St"],
                                                    "city": "PleasantVille",
                                                    "district": "Rainbow",
                                                    "state": "Vic",
                                                    "postalCode": "3999",
                                                    "period": {"start": "1974-12-25"},
                                                }
                                            ],
                                            "contact": [
                                                {
                                                    "relationship": [
                                                        {
                                                            "coding": [
                                                                {
                                                                    "system": "http://terminology.hl7.org/CodeSystem/v2-0131",
                                                                    "code": "N",
                                                                }
                                                            ]
                                                        }
                                                    ],
                                                    "name": {
                                                        "family": "du Marché",
                                                        "_family": {
                                                            "extension": [
                                                                {
                                                                    "url": "http://hl7.org/fhir/StructureDefinition/humanname-own-prefix",
                                                                    "valueString": "VV",
                                                                }
                                                            ]
                                                        },
                                                        "given": ["Bénédicte"],
                                                    },
                                                    "telecom": [
                                                        {
                                                            "system": "phone",
                                                            "value": "+33 (237) 998327",
                                                        }
                                                    ],
                                                    "address": {
                                                        "use": "home",
                                                        "type": "both",
                                                        "line": ["534 Erewhon St"],
                                                        "city": "PleasantVille",
                                                        "district": "Rainbow",
                                                        "state": "Vic",
                                                        "postalCode": "3999",
                                                        "period": {
                                                            "start": "1974-12-25"
                                                        },
                                                    },
                                                    "gender": "female",
                                                    "period": {"start": "2012"},
                                                }
                                            ],
                                            "managingOrganization": {
                                                "reference": "Organization/1"
                                            },
                                        },
                                    },
                                    "pat1": {
                                        "summary": "Patient 1 for linking",
                                        "description": "Patient 1 for linking",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-a.json",
                                    },
                                    "pat2": {
                                        "summary": "Patient 2 for linking",
                                        "description": "Patient 2 for linking",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-b.json",
                                    },
                                    "pat3": {
                                        "summary": "Deceased patient (using time)",
                                        "description": "Deceased patient (using time)",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-c.json",
                                    },
                                    "pat4": {
                                        "summary": "Deceased patient (using boolean)",
                                        "description": "Deceased patient (using boolean)",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-d.json",
                                    },
                                    "b248b1b2-1686-4b94-9936-37d7a5f94b51": {
                                        "summary": "Stock people (defined by HL7 publishing)",
                                        "description": "Stock people (defined by HL7 publishing)",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-examples-general.json",
                                    },
                                    "patient-example-sex-and-gender": {
                                        "summary": "Transgender Person Example",
                                        "description": "Transgender Person Example",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-sex-and-gender.json",
                                    },
                                    "b3f24cf14-d349-45b3-8134-3d83e9104875": {
                                        "summary": "Example People from cypress project",
                                        "description": "Example People from cypress project",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-examples-cypress-template.json",
                                    },
                                    "xcda": {
                                        "summary": "2nd person example",
                                        "description": "2nd person example",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-xcda.json",
                                    },
                                    "xds": {
                                        "summary": "XDS Patient",
                                        "description": "XDS Patient",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-xds.json",
                                    },
                                    "animal": {
                                        "summary": "An example of an animal",
                                        "description": "An example of an animal",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-animal.json",
                                    },
                                    "dicom": {
                                        "summary": "Taken from a DICOM sample",
                                        "description": "Taken from a DICOM sample",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-dicom.json",
                                    },
                                    "ihe-pcd": {
                                        "summary": "Example from IHE-PCD example",
                                        "description": "Example from IHE-PCD example",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-ihe-pcd.json",
                                    },
                                    "f001": {
                                        "summary": "Real-world patient example (anonymized)",
                                        "description": "Real-world patient example (anonymized)",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-f001-pieter.json",
                                    },
                                    "f201": {
                                        "summary": "Real-world patient example (anonymized)",
                                        "description": "Real-world patient example (anonymized)",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-f201-roel.json",
                                    },
                                    "glossy": {
                                        "summary": "Example for glossy",
                                        "description": "Example for glossy",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-glossy-example.json",
                                    },
                                    "proband": {
                                        "summary": "Genetic Risk Assessment Person",
                                        "description": "Genetic Risk Assessment Person",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-proband.json",
                                    },
                                    "genetics-example1": {
                                        "summary": "Additional Genetics Example",
                                        "description": "Additional Genetics Example",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-genetics-example1.json",
                                    },
                                    "ch-example": {
                                        "summary": "Example Patient resource with Chinese content",
                                        "description": "Example Patient resource with Chinese content",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-chinese.json",
                                    },
                                    "newborn": {
                                        "summary": "Newborn Patient Example",
                                        "description": "Newborn Patient Example",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-newborn.json",
                                    },
                                    "mom": {
                                        "summary": "Mother of Newborn Patient Example",
                                        "description": "Mother of Newborn Patient Example",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-mom.json",
                                    },
                                    "infant-twin-1": {
                                        "summary": "Newborn Eldest Twin Example",
                                        "description": "Newborn Eldest Twin Example",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-infant-twin-1.json",
                                    },
                                    "infant-twin-2": {
                                        "summary": "Newborn Youngest Twin Example",
                                        "description": "Newborn Youngest Twin Example",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-infant-twin-2.json",
                                    },
                                    "infant-fetal": {
                                        "summary": "Pre-birth fetal infant Example",
                                        "description": "Pre-birth fetal infant Example",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-infant-fetal.json",
                                    },
                                    "infant-mom": {
                                        "summary": "Mother of infant twins and fetal infant.",
                                        "description": "Mother of infant twins and fetal infant.",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-infant-mom.json",
                                    },
                                },
                            }
                        },
                    },
                    "401": {
                        "description": "Authentication is required for the Patient read interaction that was attempted.",
                        "content": {
                            "application/fhir+json": {
                                "schema": {
                                    "$ref": "#/components/schemas/OperationOutcome"
                                },
                                "example": {
                                    "resourceType": "OperationOutcome",
                                    "id": "101",
                                    "issue": [
                                        {
                                            "severity": "error",
                                            "code": "unknown",
                                            "details": {
                                                "text": "Authentication failed"
                                            },
                                        }
                                    ],
                                },
                            }
                        },
                    },
                    "403": {
                        "description": "Authorization is required for the Patient read interaction that was attempted.",
                        "content": {
                            "application/fhir+json": {
                                "schema": {
                                    "$ref": "#/components/schemas/OperationOutcome"
                                },
                                "example": {
                                    "resourceType": "OperationOutcome",
                                    "id": "101",
                                    "issue": [
                                        {
                                            "severity": "error",
                                            "code": "forbidden",
                                            "details": {"text": "Authorization failed"},
                                        }
                                    ],
                                },
                            }
                        },
                    },
                    "404": {
                        "description": "Unknown Patient resource",
                        "content": {
                            "application/fhir+json": {
                                "schema": {
                                    "$ref": "#/components/schemas/OperationOutcome"
                                },
                                "example": {
                                    "resourceType": "OperationOutcome",
                                    "id": "101",
                                    "issue": [
                                        {
                                            "severity": "error",
                                            "code": "not-found",
                                            "details": {"text": "Resource not found"},
                                        }
                                    ],
                                },
                            }
                        },
                    },
                    "500": {
                        "description": "The server has encountered a situation it does not know how to handle.",
                        "content": {
                            "application/fhir+json": {
                                "schema": {
                                    "$ref": "#/components/schemas/OperationOutcome"
                                },
                                "example": {
                                    "resourceType": "OperationOutcome",
                                    "id": "101",
                                    "issue": [
                                        {
                                            "severity": "error",
                                            "code": "exception",
                                            "details": {
                                                "text": "Internal server error"
                                            },
                                        }
                                    ],
                                },
                            }
                        },
                    },
                },
            },
            "put": {
                "tags": ["Type:Patient"],
                "summary": "Patient update",
                "description": "The Patient update interaction creates a new current version for an existing Patient resource.",
                "operationId": "fhirstarter|instance|update|put|Patient|fhir.resources.patient|Patient",
                "parameters": [
                    {
                        "description": "Logical id of this artifact",
                        "required": True,
                        "schema": {
                            "type": "string",
                            "maxLength": 64,
                            "minLength": 1,
                            "pattern": "^[A-Za-z0-9\\-.]+$",
                            "title": "Id",
                            "description": "Logical id of this artifact",
                        },
                        "name": "id",
                        "in": "path",
                    },
                    {
                        "description": "Override the HTTP content negotiation to specify JSON or XML response format",
                        "required": False,
                        "schema": {
                            "type": "string",
                            "title": " Format",
                            "description": "Override the HTTP content negotiation to specify JSON or XML response format",
                        },
                        "name": "_format",
                        "in": "query",
                    },
                    {
                        "description": "Ask for a pretty printed response for human convenience",
                        "required": False,
                        "schema": {
                            "type": "string",
                            "title": " Pretty",
                            "description": "Ask for a pretty printed response for human convenience",
                        },
                        "name": "_pretty",
                        "in": "query",
                    },
                ],
                "requestBody": {
                    "content": {
                        "application/fhir+json": {
                            "schema": {"$ref": "#/components/schemas/Patient"},
                            "examples": {
                                "example": {
                                    "summary": "General Person Example",
                                    "description": "General Person Example",
                                    "value": {
                                        "resourceType": "Patient",
                                        "id": "example",
                                        "text": {
                                            "status": "generated",
                                            "div": '<div xmlns="http://www.w3.org/1999/xhtml"><p style="border: 1px #661aff solid; background-color: #e6e6ff; padding: 10px;"><b>Jim </b> male, DoB: 1974-12-25 ( Medical record number: 12345\xa0(use:\xa0USUAL,\xa0period:\xa02001-05-06 --&gt; (ongoing)))</p><hr/><table class="grid"><tr><td style="background-color: #f3f5da" title="Record is active">Active:</td><td>true</td><td style="background-color: #f3f5da" title="Known status of Patient">Deceased:</td><td colspan="3">false</td></tr><tr><td style="background-color: #f3f5da" title="Alternate names (see the one above)">Alt Names:</td><td colspan="3"><ul><li>Peter James Chalmers (OFFICIAL)</li><li>Peter James Windsor (MAIDEN)</li></ul></td></tr><tr><td style="background-color: #f3f5da" title="Ways to contact the Patient">Contact Details:</td><td colspan="3"><ul><li>-unknown-(HOME)</li><li>ph: (03) 5555 6473(WORK)</li><li>ph: (03) 3410 5613(MOBILE)</li><li>ph: (03) 5555 8834(OLD)</li><li>534 Erewhon St PeasantVille, Rainbow, Vic  3999(HOME)</li></ul></td></tr><tr><td style="background-color: #f3f5da" title="Nominated Contact: Next-of-Kin">Next-of-Kin:</td><td colspan="3"><ul><li>Bénédicte du Marché  (female)</li><li>534 Erewhon St PleasantVille Vic 3999 (HOME)</li><li><a href="tel:+33(237)998327">+33 (237) 998327</a></li><li>Valid Period: 2012 --&gt; (ongoing)</li></ul></td></tr><tr><td style="background-color: #f3f5da" title="Patient Links">Links:</td><td colspan="3"><ul><li>Managing Organization: <a href="organization-example-gastro.html">Organization/1</a> &quot;Gastroenterology&quot;</li></ul></td></tr></table></div>',
                                        },
                                        "identifier": [
                                            {
                                                "use": "usual",
                                                "type": {
                                                    "coding": [
                                                        {
                                                            "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                                                            "code": "MR",
                                                        }
                                                    ]
                                                },
                                                "system": "urn:oid:1.2.36.146.595.217.0.1",
                                                "value": "12345",
                                                "period": {"start": "2001-05-06"},
                                                "assigner": {
                                                    "display": "Acme Healthcare"
                                                },
                                            }
                                        ],
                                        "active": True,
                                        "name": [
                                            {
                                                "use": "official",
                                                "family": "Chalmers",
                                                "given": ["Peter", "James"],
                                            },
                                            {"use": "usual", "given": ["Jim"]},
                                            {
                                                "use": "maiden",
                                                "family": "Windsor",
                                                "given": ["Peter", "James"],
                                                "period": {"end": "2002"},
                                            },
                                        ],
                                        "telecom": [
                                            {"use": "home"},
                                            {
                                                "system": "phone",
                                                "value": "(03) 5555 6473",
                                                "use": "work",
                                                "rank": 1,
                                            },
                                            {
                                                "system": "phone",
                                                "value": "(03) 3410 5613",
                                                "use": "mobile",
                                                "rank": 2,
                                            },
                                            {
                                                "system": "phone",
                                                "value": "(03) 5555 8834",
                                                "use": "old",
                                                "period": {"end": "2014"},
                                            },
                                        ],
                                        "gender": "male",
                                        "birthDate": "1974-12-25",
                                        "_birthDate": {
                                            "extension": [
                                                {
                                                    "url": "http://hl7.org/fhir/StructureDefinition/patient-birthTime",
                                                    "valueDateTime": "1974-12-25T14:35:45-05:00",
                                                }
                                            ]
                                        },
                                        "deceasedBoolean": False,
                                        "address": [
                                            {
                                                "use": "home",
                                                "type": "both",
                                                "text": "534 Erewhon St PeasantVille, Rainbow, Vic  3999",
                                                "line": ["534 Erewhon St"],
                                                "city": "PleasantVille",
                                                "district": "Rainbow",
                                                "state": "Vic",
                                                "postalCode": "3999",
                                                "period": {"start": "1974-12-25"},
                                            }
                                        ],
                                        "contact": [
                                            {
                                                "relationship": [
                                                    {
                                                        "coding": [
                                                            {
                                                                "system": "http://terminology.hl7.org/CodeSystem/v2-0131",
                                                                "code": "N",
                                                            }
                                                        ]
                                                    }
                                                ],
                                                "name": {
                                                    "family": "du Marché",
                                                    "_family": {
                                                        "extension": [
                                                            {
                                                                "url": "http://hl7.org/fhir/StructureDefinition/humanname-own-prefix",
                                                                "valueString": "VV",
                                                            }
                                                        ]
                                                    },
                                                    "given": ["Bénédicte"],
                                                },
                                                "telecom": [
                                                    {
                                                        "system": "phone",
                                                        "value": "+33 (237) 998327",
                                                    }
                                                ],
                                                "address": {
                                                    "use": "home",
                                                    "type": "both",
                                                    "line": ["534 Erewhon St"],
                                                    "city": "PleasantVille",
                                                    "district": "Rainbow",
                                                    "state": "Vic",
                                                    "postalCode": "3999",
                                                    "period": {"start": "1974-12-25"},
                                                },
                                                "gender": "female",
                                                "period": {"start": "2012"},
                                            }
                                        ],
                                        "managingOrganization": {
                                            "reference": "Organization/1"
                                        },
                                    },
                                },
                                "pat1": {
                                    "summary": "Patient 1 for linking",
                                    "description": "Patient 1 for linking",
                                    "externalValue": "https://hl7.org/fhir/R5/patient-example-a.json",
                                },
                                "pat2": {
                                    "summary": "Patient 2 for linking",
                                    "description": "Patient 2 for linking",
                                    "externalValue": "https://hl7.org/fhir/R5/patient-example-b.json",
                                },
                                "pat3": {
                                    "summary": "Deceased patient (using time)",
                                    "description": "Deceased patient (using time)",
                                    "externalValue": "https://hl7.org/fhir/R5/patient-example-c.json",
                                },
                                "pat4": {
                                    "summary": "Deceased patient (using boolean)",
                                    "description": "Deceased patient (using boolean)",
                                    "externalValue": "https://hl7.org/fhir/R5/patient-example-d.json",
                                },
                                "b248b1b2-1686-4b94-9936-37d7a5f94b51": {
                                    "summary": "Stock people (defined by HL7 publishing)",
                                    "description": "Stock people (defined by HL7 publishing)",
                                    "externalValue": "https://hl7.org/fhir/R5/patient-examples-general.json",
                                },
                                "patient-example-sex-and-gender": {
                                    "summary": "Transgender Person Example",
                                    "description": "Transgender Person Example",
                                    "externalValue": "https://hl7.org/fhir/R5/patient-example-sex-and-gender.json",
                                },
                                "b3f24cf14-d349-45b3-8134-3d83e9104875": {
                                    "summary": "Example People from cypress project",
                                    "description": "Example People from cypress project",
                                    "externalValue": "https://hl7.org/fhir/R5/patient-examples-cypress-template.json",
                                },
                                "xcda": {
                                    "summary": "2nd person example",
                                    "description": "2nd person example",
                                    "externalValue": "https://hl7.org/fhir/R5/patient-example-xcda.json",
                                },
                                "xds": {
                                    "summary": "XDS Patient",
                                    "description": "XDS Patient",
                                    "externalValue": "https://hl7.org/fhir/R5/patient-example-xds.json",
                                },
                                "animal": {
                                    "summary": "An example of an animal",
                                    "description": "An example of an animal",
                                    "externalValue": "https://hl7.org/fhir/R5/patient-example-animal.json",
                                },
                                "dicom": {
                                    "summary": "Taken from a DICOM sample",
                                    "description": "Taken from a DICOM sample",
                                    "externalValue": "https://hl7.org/fhir/R5/patient-example-dicom.json",
                                },
                                "ihe-pcd": {
                                    "summary": "Example from IHE-PCD example",
                                    "description": "Example from IHE-PCD example",
                                    "externalValue": "https://hl7.org/fhir/R5/patient-example-ihe-pcd.json",
                                },
                                "f001": {
                                    "summary": "Real-world patient example (anonymized)",
                                    "description": "Real-world patient example (anonymized)",
                                    "externalValue": "https://hl7.org/fhir/R5/patient-example-f001-pieter.json",
                                },
                                "f201": {
                                    "summary": "Real-world patient example (anonymized)",
                                    "description": "Real-world patient example (anonymized)",
                                    "externalValue": "https://hl7.org/fhir/R5/patient-example-f201-roel.json",
                                },
                                "glossy": {
                                    "summary": "Example for glossy",
                                    "description": "Example for glossy",
                                    "externalValue": "https://hl7.org/fhir/R5/patient-glossy-example.json",
                                },
                                "proband": {
                                    "summary": "Genetic Risk Assessment Person",
                                    "description": "Genetic Risk Assessment Person",
                                    "externalValue": "https://hl7.org/fhir/R5/patient-example-proband.json",
                                },
                                "genetics-example1": {
                                    "summary": "Additional Genetics Example",
                                    "description": "Additional Genetics Example",
                                    "externalValue": "https://hl7.org/fhir/R5/patient-genetics-example1.json",
                                },
                                "ch-example": {
                                    "summary": "Example Patient resource with Chinese content",
                                    "description": "Example Patient resource with Chinese content",
                                    "externalValue": "https://hl7.org/fhir/R5/patient-example-chinese.json",
                                },
                                "newborn": {
                                    "summary": "Newborn Patient Example",
                                    "description": "Newborn Patient Example",
                                    "externalValue": "https://hl7.org/fhir/R5/patient-example-newborn.json",
                                },
                                "mom": {
                                    "summary": "Mother of Newborn Patient Example",
                                    "description": "Mother of Newborn Patient Example",
                                    "externalValue": "https://hl7.org/fhir/R5/patient-example-mom.json",
                                },
                                "infant-twin-1": {
                                    "summary": "Newborn Eldest Twin Example",
                                    "description": "Newborn Eldest Twin Example",
                                    "externalValue": "https://hl7.org/fhir/R5/patient-example-infant-twin-1.json",
                                },
                                "infant-twin-2": {
                                    "summary": "Newborn Youngest Twin Example",
                                    "description": "Newborn Youngest Twin Example",
                                    "externalValue": "https://hl7.org/fhir/R5/patient-example-infant-twin-2.json",
                                },
                                "infant-fetal": {
                                    "summary": "Pre-birth fetal infant Example",
                                    "description": "Pre-birth fetal infant Example",
                                    "externalValue": "https://hl7.org/fhir/R5/patient-example-infant-fetal.json",
                                },
                                "infant-mom": {
                                    "summary": "Mother of infant twins and fetal infant.",
                                    "description": "Mother of infant twins and fetal infant.",
                                    "externalValue": "https://hl7.org/fhir/R5/patient-example-infant-mom.json",
                                },
                            },
                        }
                    },
                    "required": True,
                },
                "responses": {
                    "200": {
                        "description": "Successful Patient update",
                        "content": {
                            "application/fhir+json": {
                                "schema": {"$ref": "#/components/schemas/Patient"},
                                "examples": {
                                    "example": {
                                        "summary": "General Person Example",
                                        "description": "General Person Example",
                                        "value": {
                                            "resourceType": "Patient",
                                            "id": "example",
                                            "text": {
                                                "status": "generated",
                                                "div": '<div xmlns="http://www.w3.org/1999/xhtml"><p style="border: 1px #661aff solid; background-color: #e6e6ff; padding: 10px;"><b>Jim </b> male, DoB: 1974-12-25 ( Medical record number: 12345\xa0(use:\xa0USUAL,\xa0period:\xa02001-05-06 --&gt; (ongoing)))</p><hr/><table class="grid"><tr><td style="background-color: #f3f5da" title="Record is active">Active:</td><td>true</td><td style="background-color: #f3f5da" title="Known status of Patient">Deceased:</td><td colspan="3">false</td></tr><tr><td style="background-color: #f3f5da" title="Alternate names (see the one above)">Alt Names:</td><td colspan="3"><ul><li>Peter James Chalmers (OFFICIAL)</li><li>Peter James Windsor (MAIDEN)</li></ul></td></tr><tr><td style="background-color: #f3f5da" title="Ways to contact the Patient">Contact Details:</td><td colspan="3"><ul><li>-unknown-(HOME)</li><li>ph: (03) 5555 6473(WORK)</li><li>ph: (03) 3410 5613(MOBILE)</li><li>ph: (03) 5555 8834(OLD)</li><li>534 Erewhon St PeasantVille, Rainbow, Vic  3999(HOME)</li></ul></td></tr><tr><td style="background-color: #f3f5da" title="Nominated Contact: Next-of-Kin">Next-of-Kin:</td><td colspan="3"><ul><li>Bénédicte du Marché  (female)</li><li>534 Erewhon St PleasantVille Vic 3999 (HOME)</li><li><a href="tel:+33(237)998327">+33 (237) 998327</a></li><li>Valid Period: 2012 --&gt; (ongoing)</li></ul></td></tr><tr><td style="background-color: #f3f5da" title="Patient Links">Links:</td><td colspan="3"><ul><li>Managing Organization: <a href="organization-example-gastro.html">Organization/1</a> &quot;Gastroenterology&quot;</li></ul></td></tr></table></div>',
                                            },
                                            "identifier": [
                                                {
                                                    "use": "usual",
                                                    "type": {
                                                        "coding": [
                                                            {
                                                                "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                                                                "code": "MR",
                                                            }
                                                        ]
                                                    },
                                                    "system": "urn:oid:1.2.36.146.595.217.0.1",
                                                    "value": "12345",
                                                    "period": {"start": "2001-05-06"},
                                                    "assigner": {
                                                        "display": "Acme Healthcare"
                                                    },
                                                }
                                            ],
                                            "active": True,
                                            "name": [
                                                {
                                                    "use": "official",
                                                    "family": "Chalmers",
                                                    "given": ["Peter", "James"],
                                                },
                                                {"use": "usual", "given": ["Jim"]},
                                                {
                                                    "use": "maiden",
                                                    "family": "Windsor",
                                                    "given": ["Peter", "James"],
                                                    "period": {"end": "2002"},
                                                },
                                            ],
                                            "telecom": [
                                                {"use": "home"},
                                                {
                                                    "system": "phone",
                                                    "value": "(03) 5555 6473",
                                                    "use": "work",
                                                    "rank": 1,
                                                },
                                                {
                                                    "system": "phone",
                                                    "value": "(03) 3410 5613",
                                                    "use": "mobile",
                                                    "rank": 2,
                                                },
                                                {
                                                    "system": "phone",
                                                    "value": "(03) 5555 8834",
                                                    "use": "old",
                                                    "period": {"end": "2014"},
                                                },
                                            ],
                                            "gender": "male",
                                            "birthDate": "1974-12-25",
                                            "_birthDate": {
                                                "extension": [
                                                    {
                                                        "url": "http://hl7.org/fhir/StructureDefinition/patient-birthTime",
                                                        "valueDateTime": "1974-12-25T14:35:45-05:00",
                                                    }
                                                ]
                                            },
                                            "deceasedBoolean": False,
                                            "address": [
                                                {
                                                    "use": "home",
                                                    "type": "both",
                                                    "text": "534 Erewhon St PeasantVille, Rainbow, Vic  3999",
                                                    "line": ["534 Erewhon St"],
                                                    "city": "PleasantVille",
                                                    "district": "Rainbow",
                                                    "state": "Vic",
                                                    "postalCode": "3999",
                                                    "period": {"start": "1974-12-25"},
                                                }
                                            ],
                                            "contact": [
                                                {
                                                    "relationship": [
                                                        {
                                                            "coding": [
                                                                {
                                                                    "system": "http://terminology.hl7.org/CodeSystem/v2-0131",
                                                                    "code": "N",
                                                                }
                                                            ]
                                                        }
                                                    ],
                                                    "name": {
                                                        "family": "du Marché",
                                                        "_family": {
                                                            "extension": [
                                                                {
                                                                    "url": "http://hl7.org/fhir/StructureDefinition/humanname-own-prefix",
                                                                    "valueString": "VV",
                                                                }
                                                            ]
                                                        },
                                                        "given": ["Bénédicte"],
                                                    },
                                                    "telecom": [
                                                        {
                                                            "system": "phone",
                                                            "value": "+33 (237) 998327",
                                                        }
                                                    ],
                                                    "address": {
                                                        "use": "home",
                                                        "type": "both",
                                                        "line": ["534 Erewhon St"],
                                                        "city": "PleasantVille",
                                                        "district": "Rainbow",
                                                        "state": "Vic",
                                                        "postalCode": "3999",
                                                        "period": {
                                                            "start": "1974-12-25"
                                                        },
                                                    },
                                                    "gender": "female",
                                                    "period": {"start": "2012"},
                                                }
                                            ],
                                            "managingOrganization": {
                                                "reference": "Organization/1"
                                            },
                                        },
                                    },
                                    "pat1": {
                                        "summary": "Patient 1 for linking",
                                        "description": "Patient 1 for linking",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-a.json",
                                    },
                                    "pat2": {
                                        "summary": "Patient 2 for linking",
                                        "description": "Patient 2 for linking",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-b.json",
                                    },
                                    "pat3": {
                                        "summary": "Deceased patient (using time)",
                                        "description": "Deceased patient (using time)",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-c.json",
                                    },
                                    "pat4": {
                                        "summary": "Deceased patient (using boolean)",
                                        "description": "Deceased patient (using boolean)",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-d.json",
                                    },
                                    "b248b1b2-1686-4b94-9936-37d7a5f94b51": {
                                        "summary": "Stock people (defined by HL7 publishing)",
                                        "description": "Stock people (defined by HL7 publishing)",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-examples-general.json",
                                    },
                                    "patient-example-sex-and-gender": {
                                        "summary": "Transgender Person Example",
                                        "description": "Transgender Person Example",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-sex-and-gender.json",
                                    },
                                    "b3f24cf14-d349-45b3-8134-3d83e9104875": {
                                        "summary": "Example People from cypress project",
                                        "description": "Example People from cypress project",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-examples-cypress-template.json",
                                    },
                                    "xcda": {
                                        "summary": "2nd person example",
                                        "description": "2nd person example",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-xcda.json",
                                    },
                                    "xds": {
                                        "summary": "XDS Patient",
                                        "description": "XDS Patient",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-xds.json",
                                    },
                                    "animal": {
                                        "summary": "An example of an animal",
                                        "description": "An example of an animal",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-animal.json",
                                    },
                                    "dicom": {
                                        "summary": "Taken from a DICOM sample",
                                        "description": "Taken from a DICOM sample",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-dicom.json",
                                    },
                                    "ihe-pcd": {
                                        "summary": "Example from IHE-PCD example",
                                        "description": "Example from IHE-PCD example",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-ihe-pcd.json",
                                    },
                                    "f001": {
                                        "summary": "Real-world patient example (anonymized)",
                                        "description": "Real-world patient example (anonymized)",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-f001-pieter.json",
                                    },
                                    "f201": {
                                        "summary": "Real-world patient example (anonymized)",
                                        "description": "Real-world patient example (anonymized)",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-f201-roel.json",
                                    },
                                    "glossy": {
                                        "summary": "Example for glossy",
                                        "description": "Example for glossy",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-glossy-example.json",
                                    },
                                    "proband": {
                                        "summary": "Genetic Risk Assessment Person",
                                        "description": "Genetic Risk Assessment Person",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-proband.json",
                                    },
                                    "genetics-example1": {
                                        "summary": "Additional Genetics Example",
                                        "description": "Additional Genetics Example",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-genetics-example1.json",
                                    },
                                    "ch-example": {
                                        "summary": "Example Patient resource with Chinese content",
                                        "description": "Example Patient resource with Chinese content",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-chinese.json",
                                    },
                                    "newborn": {
                                        "summary": "Newborn Patient Example",
                                        "description": "Newborn Patient Example",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-newborn.json",
                                    },
                                    "mom": {
                                        "summary": "Mother of Newborn Patient Example",
                                        "description": "Mother of Newborn Patient Example",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-mom.json",
                                    },
                                    "infant-twin-1": {
                                        "summary": "Newborn Eldest Twin Example",
                                        "description": "Newborn Eldest Twin Example",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-infant-twin-1.json",
                                    },
                                    "infant-twin-2": {
                                        "summary": "Newborn Youngest Twin Example",
                                        "description": "Newborn Youngest Twin Example",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-infant-twin-2.json",
                                    },
                                    "infant-fetal": {
                                        "summary": "Pre-birth fetal infant Example",
                                        "description": "Pre-birth fetal infant Example",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-infant-fetal.json",
                                    },
                                    "infant-mom": {
                                        "summary": "Mother of infant twins and fetal infant.",
                                        "description": "Mother of infant twins and fetal infant.",
                                        "externalValue": "https://hl7.org/fhir/R5/patient-example-infant-mom.json",
                                    },
                                },
                            }
                        },
                    },
                    "400": {
                        "description": "Patient update request could not be parsed or failed basic FHIR validation rules.",
                        "content": {
                            "application/fhir+json": {
                                "schema": {
                                    "$ref": "#/components/schemas/OperationOutcome"
                                },
                                "example": {
                                    "resourceType": "OperationOutcome",
                                    "id": "101",
                                    "issue": [
                                        {
                                            "severity": "error",
                                            "code": "invalid",
                                            "details": {"text": "Bad request"},
                                        }
                                    ],
                                },
                            }
                        },
                    },
                    "401": {
                        "description": "Authentication is required for the Patient update interaction that was attempted.",
                        "content": {
                            "application/fhir+json": {
                                "schema": {
                                    "$ref": "#/components/schemas/OperationOutcome"
                                },
                                "example": {
                                    "resourceType": "OperationOutcome",
                                    "id": "101",
                                    "issue": [
                                        {
                                            "severity": "error",
                                            "code": "unknown",
                                            "details": {
                                                "text": "Authentication failed"
                                            },
                                        }
                                    ],
                                },
                            }
                        },
                    },
                    "403": {
                        "description": "Authorization is required for the Patient update interaction that was attempted.",
                        "content": {
                            "application/fhir+json": {
                                "schema": {
                                    "$ref": "#/components/schemas/OperationOutcome"
                                },
                                "example": {
                                    "resourceType": "OperationOutcome",
                                    "id": "101",
                                    "issue": [
                                        {
                                            "severity": "error",
                                            "code": "forbidden",
                                            "details": {"text": "Authorization failed"},
                                        }
                                    ],
                                },
                            }
                        },
                    },
                    "422": {
                        "description": "The proposed Patient resource violated applicable FHIR profiles or server business rules.",
                        "content": {
                            "application/fhir+json": {
                                "schema": {
                                    "$ref": "#/components/schemas/OperationOutcome"
                                },
                                "example": {
                                    "resourceType": "OperationOutcome",
                                    "id": "101",
                                    "issue": [
                                        {
                                            "severity": "error",
                                            "code": "processing",
                                            "details": {"text": "Unprocessable entity"},
                                        }
                                    ],
                                },
                            }
                        },
                    },
                    "500": {
                        "description": "The server has encountered a situation it does not know how to handle.",
                        "content": {
                            "application/fhir+json": {
                                "schema": {
                                    "$ref": "#/components/schemas/OperationOutcome"
                                },
                                "example": {
                                    "resourceType": "OperationOutcome",
                                    "id": "101",
                                    "issue": [
                                        {
                                            "severity": "error",
                                            "code": "exception",
                                            "details": {
                                                "text": "Internal server error"
                                            },
                                        }
                                    ],
                                },
                            }
                        },
                    },
                },
            },
        },
        "/Patient/_search": {
            "post": {
                "tags": ["Type:Patient"],
                "summary": "Patient search-type",
                "description": "The Patient search-type interaction searches a set of resources based on some filter criteria.",
                "operationId": "fhirstarter|type|search-type|post|Patient|fhir.resources.patient|Patient",
                "requestBody": {
                    "content": {
                        "application/x-www-form-urlencoded": {
                            "schema": {
                                "properties": {
                                    "family": {
                                        "type": "string",
                                        "title": "Family",
                                        "description": "A portion of the family name of the patient",
                                    },
                                    "general-practitioner": {
                                        "type": "string",
                                        "title": "General-Practitioner",
                                        "description": "Patient's nominated general practitioner, not the organization that manages the record",
                                    },
                                    "nickname": {
                                        "type": "string",
                                        "title": "Nickname",
                                        "description": "Nickname",
                                    },
                                    "_lastUpdated": {
                                        "type": "string",
                                        "title": " Lastupdated",
                                        "description": "When the resource version last changed",
                                    },
                                    "_format": {
                                        "type": "string",
                                        "title": " Format",
                                        "description": "Override the HTTP content negotiation to specify JSON or XML response format",
                                    },
                                    "_pretty": {
                                        "type": "string",
                                        "title": " Pretty",
                                        "description": "Ask for a pretty printed response for human convenience",
                                    },
                                },
                                "type": "object",
                                "title": "Body_fhirstarter|type|search-type|post|Patient|fhir.resources.patient|Patient",
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Successful Patient search-type",
                        "content": {
                            "application/fhir+json": {
                                "schema": {"$ref": "#/components/schemas/Bundle"},
                                "example": {
                                    "resourceType": "Bundle",
                                    "id": "bundle-example",
                                    "meta": {"lastUpdated": "2014-08-18T01:43:30Z"},
                                    "type": "searchset",
                                    "total": 3,
                                    "link": [
                                        {
                                            "relation": "self",
                                            "url": "https://example.com/base/Patient?_count=1",
                                        },
                                        {
                                            "relation": "next",
                                            "url": "https://example.com/base/Patient?searchId=ff15fd40-ff71-4b48-b366-09c706bed9d0&page=2",
                                        },
                                    ],
                                    "entry": [
                                        {
                                            "fullUrl": "https://example.com/base/Patient/example",
                                            "resource": {
                                                "resourceType": "Patient",
                                                "id": "example",
                                                "text": {
                                                    "status": "generated",
                                                    "div": '<div xmlns="http://www.w3.org/1999/xhtml"><p style="border: 1px #661aff solid; background-color: #e6e6ff; padding: 10px;"><b>Jim </b> male, DoB: 1974-12-25 ( Medical record number: 12345\xa0(use:\xa0USUAL,\xa0period:\xa02001-05-06 --&gt; (ongoing)))</p><hr/><table class="grid"><tr><td style="background-color: #f3f5da" title="Record is active">Active:</td><td>true</td><td style="background-color: #f3f5da" title="Known status of Patient">Deceased:</td><td colspan="3">false</td></tr><tr><td style="background-color: #f3f5da" title="Alternate names (see the one above)">Alt Names:</td><td colspan="3"><ul><li>Peter James Chalmers (OFFICIAL)</li><li>Peter James Windsor (MAIDEN)</li></ul></td></tr><tr><td style="background-color: #f3f5da" title="Ways to contact the Patient">Contact Details:</td><td colspan="3"><ul><li>-unknown-(HOME)</li><li>ph: (03) 5555 6473(WORK)</li><li>ph: (03) 3410 5613(MOBILE)</li><li>ph: (03) 5555 8834(OLD)</li><li>534 Erewhon St PeasantVille, Rainbow, Vic  3999(HOME)</li></ul></td></tr><tr><td style="background-color: #f3f5da" title="Nominated Contact: Next-of-Kin">Next-of-Kin:</td><td colspan="3"><ul><li>Bénédicte du Marché  (female)</li><li>534 Erewhon St PleasantVille Vic 3999 (HOME)</li><li><a href="tel:+33(237)998327">+33 (237) 998327</a></li><li>Valid Period: 2012 --&gt; (ongoing)</li></ul></td></tr><tr><td style="background-color: #f3f5da" title="Patient Links">Links:</td><td colspan="3"><ul><li>Managing Organization: <a href="organization-example-gastro.html">Organization/1</a> &quot;Gastroenterology&quot;</li></ul></td></tr></table></div>',
                                                },
                                                "identifier": [
                                                    {
                                                        "use": "usual",
                                                        "type": {
                                                            "coding": [
                                                                {
                                                                    "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                                                                    "code": "MR",
                                                                }
                                                            ]
                                                        },
                                                        "system": "urn:oid:1.2.36.146.595.217.0.1",
                                                        "value": "12345",
                                                        "period": {
                                                            "start": "2001-05-06"
                                                        },
                                                        "assigner": {
                                                            "display": "Acme Healthcare"
                                                        },
                                                    }
                                                ],
                                                "active": True,
                                                "name": [
                                                    {
                                                        "use": "official",
                                                        "family": "Chalmers",
                                                        "given": ["Peter", "James"],
                                                    },
                                                    {"use": "usual", "given": ["Jim"]},
                                                    {
                                                        "use": "maiden",
                                                        "family": "Windsor",
                                                        "given": ["Peter", "James"],
                                                        "period": {"end": "2002"},
                                                    },
                                                ],
                                                "telecom": [
                                                    {"use": "home"},
                                                    {
                                                        "system": "phone",
                                                        "value": "(03) 5555 6473",
                                                        "use": "work",
                                                        "rank": 1,
                                                    },
                                                    {
                                                        "system": "phone",
                                                        "value": "(03) 3410 5613",
                                                        "use": "mobile",
                                                        "rank": 2,
                                                    },
                                                    {
                                                        "system": "phone",
                                                        "value": "(03) 5555 8834",
                                                        "use": "old",
                                                        "period": {"end": "2014"},
                                                    },
                                                ],
                                                "gender": "male",
                                                "birthDate": "1974-12-25",
                                                "_birthDate": {
                                                    "extension": [
                                                        {
                                                            "url": "http://hl7.org/fhir/StructureDefinition/patient-birthTime",
                                                            "valueDateTime": "1974-12-25T14:35:45-05:00",
                                                        }
                                                    ]
                                                },
                                                "deceasedBoolean": False,
                                                "address": [
                                                    {
                                                        "use": "home",
                                                        "type": "both",
                                                        "text": "534 Erewhon St PeasantVille, Rainbow, Vic  3999",
                                                        "line": ["534 Erewhon St"],
                                                        "city": "PleasantVille",
                                                        "district": "Rainbow",
                                                        "state": "Vic",
                                                        "postalCode": "3999",
                                                        "period": {
                                                            "start": "1974-12-25"
                                                        },
                                                    }
                                                ],
                                                "contact": [
                                                    {
                                                        "relationship": [
                                                            {
                                                                "coding": [
                                                                    {
                                                                        "system": "http://terminology.hl7.org/CodeSystem/v2-0131",
                                                                        "code": "N",
                                                                    }
                                                                ]
                                                            }
                                                        ],
                                                        "name": {
                                                            "family": "du Marché",
                                                            "_family": {
                                                                "extension": [
                                                                    {
                                                                        "url": "http://hl7.org/fhir/StructureDefinition/humanname-own-prefix",
                                                                        "valueString": "VV",
                                                                    }
                                                                ]
                                                            },
                                                            "given": ["Bénédicte"],
                                                        },
                                                        "telecom": [
                                                            {
                                                                "system": "phone",
                                                                "value": "+33 (237) 998327",
                                                            }
                                                        ],
                                                        "address": {
                                                            "use": "home",
                                                            "type": "both",
                                                            "line": ["534 Erewhon St"],
                                                            "city": "PleasantVille",
                                                            "district": "Rainbow",
                                                            "state": "Vic",
                                                            "postalCode": "3999",
                                                            "period": {
                                                                "start": "1974-12-25"
                                                            },
                                                        },
                                                        "gender": "female",
                                                        "period": {"start": "2012"},
                                                    }
                                                ],
                                                "managingOrganization": {
                                                    "reference": "Organization/1"
                                                },
                                            },
                                            "search": {"mode": "match", "score": 1},
                                        }
                                    ],
                                },
                            }
                        },
                    },
                    "400": {
                        "description": "Patient search-type request could not be parsed or failed basic FHIR validation rules.",
                        "content": {
                            "application/fhir+json": {
                                "schema": {
                                    "$ref": "#/components/schemas/OperationOutcome"
                                },
                                "example": {
                                    "resourceType": "OperationOutcome",
                                    "id": "101",
                                    "issue": [
                                        {
                                            "severity": "error",
                                            "code": "invalid",
                                            "details": {"text": "Bad request"},
                                        }
                                    ],
                                },
                            }
                        },
                    },
                    "401": {
                        "description": "Authentication is required for the Patient search-type interaction that was attempted.",
                        "content": {
                            "application/fhir+json": {
                                "schema": {
                                    "$ref": "#/components/schemas/OperationOutcome"
                                },
                                "example": {
                                    "resourceType": "OperationOutcome",
                                    "id": "101",
                                    "issue": [
                                        {
                                            "severity": "error",
                                            "code": "unknown",
                                            "details": {
                                                "text": "Authentication failed"
                                            },
                                        }
                                    ],
                                },
                            }
                        },
                    },
                    "403": {
                        "description": "Authorization is required for the Patient search-type interaction that was attempted.",
                        "content": {
                            "application/fhir+json": {
                                "schema": {
                                    "$ref": "#/components/schemas/OperationOutcome"
                                },
                                "example": {
                                    "resourceType": "OperationOutcome",
                                    "id": "101",
                                    "issue": [
                                        {
                                            "severity": "error",
                                            "code": "forbidden",
                                            "details": {"text": "Authorization failed"},
                                        }
                                    ],
                                },
                            }
                        },
                    },
                    "500": {
                        "description": "The server has encountered a situation it does not know how to handle.",
                        "content": {
                            "application/fhir+json": {
                                "schema": {
                                    "$ref": "#/components/schemas/OperationOutcome"
                                },
                                "example": {
                                    "resourceType": "OperationOutcome",
                                    "id": "101",
                                    "issue": [
                                        {
                                            "severity": "error",
                                            "code": "exception",
                                            "details": {
                                                "text": "Internal server error"
                                            },
                                        }
                                    ],
                                },
                            }
                        },
                    },
                },
            }
        },
        "/Appointment": {
            "get": {
                "tags": ["Type:Appointment"],
                "summary": "Appointment search-type",
                "description": "The Appointment search-type interaction searches a set of resources based on some filter criteria.",
                "operationId": "fhirstarter|type|search-type|get|Appointment|fhir.resources.appointment|Appointment",
                "parameters": [
                    {
                        "description": "Override the HTTP content negotiation to specify JSON or XML response format",
                        "required": False,
                        "schema": {
                            "type": "string",
                            "title": " Format",
                            "description": "Override the HTTP content negotiation to specify JSON or XML response format",
                        },
                        "name": "_format",
                        "in": "query",
                    },
                    {
                        "description": "Ask for a pretty printed response for human convenience",
                        "required": False,
                        "schema": {
                            "type": "string",
                            "title": " Pretty",
                            "description": "Ask for a pretty printed response for human convenience",
                        },
                        "name": "_pretty",
                        "in": "query",
                    },
                ],
                "responses": {
                    "200": {
                        "description": "Successful Appointment search-type",
                        "content": {
                            "application/fhir+json": {
                                "schema": {"$ref": "#/components/schemas/Bundle"},
                                "example": {
                                    "resourceType": "Bundle",
                                    "id": "bundle-example",
                                    "meta": {"lastUpdated": "2014-08-18T01:43:30Z"},
                                    "type": "searchset",
                                    "total": 3,
                                    "link": [
                                        {
                                            "relation": "self",
                                            "url": "https://example.com/base/Appointment?_count=1",
                                        },
                                        {
                                            "relation": "next",
                                            "url": "https://example.com/base/Appointment?searchId=ff15fd40-ff71-4b48-b366-09c706bed9d0&page=2",
                                        },
                                    ],
                                    "entry": [
                                        {
                                            "fullUrl": "https://example.com/base/Appointment/example",
                                            "resource": {
                                                "resourceType": "Appointment",
                                                "id": "example",
                                                "text": {
                                                    "status": "generated",
                                                    "div": '<div xmlns="http://www.w3.org/1999/xhtml">Brian MRI results discussion</div>',
                                                },
                                                "status": "booked",
                                                "class": [
                                                    {
                                                        "coding": [
                                                            {
                                                                "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
                                                                "code": "AMB",
                                                                "display": "ambulatory",
                                                            }
                                                        ]
                                                    }
                                                ],
                                                "serviceCategory": [
                                                    {
                                                        "coding": [
                                                            {
                                                                "system": "http://example.org/service-category",
                                                                "code": "gp",
                                                                "display": "General Practice",
                                                            }
                                                        ]
                                                    }
                                                ],
                                                "serviceType": [
                                                    {
                                                        "concept": {
                                                            "coding": [
                                                                {
                                                                    "code": "52",
                                                                    "display": "General Discussion",
                                                                }
                                                            ]
                                                        }
                                                    }
                                                ],
                                                "specialty": [
                                                    {
                                                        "coding": [
                                                            {
                                                                "system": "http://snomed.info/sct",
                                                                "code": "394814009",
                                                                "display": "General practice",
                                                            }
                                                        ]
                                                    }
                                                ],
                                                "appointmentType": {
                                                    "coding": [
                                                        {
                                                            "system": "http://terminology.hl7.org/CodeSystem/v2-0276",
                                                            "code": "FOLLOWUP",
                                                            "display": "A follow up visit from a previous appointment",
                                                        }
                                                    ]
                                                },
                                                "reason": [
                                                    {
                                                        "reference": {
                                                            "reference": "Condition/example",
                                                            "display": "Severe burn of left ear",
                                                        }
                                                    }
                                                ],
                                                "description": "Discussion on the results of your recent MRI",
                                                "start": "2013-12-10T09:00:00Z",
                                                "end": "2013-12-10T11:00:00Z",
                                                "created": "2013-10-10",
                                                "note": [
                                                    {
                                                        "text": "Further expand on the results of the MRI and determine the next actions that may be appropriate."
                                                    }
                                                ],
                                                "patientInstruction": [
                                                    {
                                                        "concept": {
                                                            "text": "Please avoid excessive travel (specifically flying) before this appointment"
                                                        }
                                                    }
                                                ],
                                                "basedOn": [
                                                    {
                                                        "reference": "ServiceRequest/myringotomy"
                                                    }
                                                ],
                                                "subject": {
                                                    "reference": "Patient/example",
                                                    "display": "Peter James Chalmers",
                                                },
                                                "participant": [
                                                    {
                                                        "actor": {
                                                            "reference": "Patient/example",
                                                            "display": "Peter James Chalmers",
                                                        },
                                                        "required": True,
                                                        "status": "accepted",
                                                    },
                                                    {
                                                        "type": [
                                                            {
                                                                "coding": [
                                                                    {
                                                                        "system": "http://terminology.hl7.org/CodeSystem/v3-ParticipationType",
                                                                        "code": "ATND",
                                                                    }
                                                                ]
                                                            }
                                                        ],
                                                        "actor": {
                                                            "reference": "Practitioner/example",
                                                            "display": "Dr Adam Careful",
                                                        },
                                                        "required": True,
                                                        "status": "accepted",
                                                    },
                                                    {
                                                        "actor": {
                                                            "reference": "Location/1",
                                                            "display": "South Wing, second floor",
                                                        },
                                                        "required": True,
                                                        "status": "accepted",
                                                    },
                                                ],
                                            },
                                            "search": {"mode": "match", "score": 1},
                                        }
                                    ],
                                },
                            }
                        },
                    },
                    "400": {
                        "description": "Appointment search-type request could not be parsed or failed basic FHIR validation rules.",
                        "content": {
                            "application/fhir+json": {
                                "schema": {
                                    "$ref": "#/components/schemas/OperationOutcome"
                                },
                                "example": {
                                    "resourceType": "OperationOutcome",
                                    "id": "101",
                                    "issue": [
                                        {
                                            "severity": "error",
                                            "code": "invalid",
                                            "details": {"text": "Bad request"},
                                        }
                                    ],
                                },
                            }
                        },
                    },
                    "401": {
                        "description": "Authentication is required for the Appointment search-type interaction that was attempted.",
                        "content": {
                            "application/fhir+json": {
                                "schema": {
                                    "$ref": "#/components/schemas/OperationOutcome"
                                },
                                "example": {
                                    "resourceType": "OperationOutcome",
                                    "id": "101",
                                    "issue": [
                                        {
                                            "severity": "error",
                                            "code": "unknown",
                                            "details": {
                                                "text": "Authentication failed"
                                            },
                                        }
                                    ],
                                },
                            }
                        },
                    },
                    "403": {
                        "description": "Authorization is required for the Appointment search-type interaction that was attempted.",
                        "content": {
                            "application/fhir+json": {
                                "schema": {
                                    "$ref": "#/components/schemas/OperationOutcome"
                                },
                                "example": {
                                    "resourceType": "OperationOutcome",
                                    "id": "101",
                                    "issue": [
                                        {
                                            "severity": "error",
                                            "code": "forbidden",
                                            "details": {"text": "Authorization failed"},
                                        }
                                    ],
                                },
                            }
                        },
                    },
                    "500": {
                        "description": "The server has encountered a situation it does not know how to handle.",
                        "content": {
                            "application/fhir+json": {
                                "schema": {
                                    "$ref": "#/components/schemas/OperationOutcome"
                                },
                                "example": {
                                    "resourceType": "OperationOutcome",
                                    "id": "101",
                                    "issue": [
                                        {
                                            "severity": "error",
                                            "code": "exception",
                                            "details": {
                                                "text": "Internal server error"
                                            },
                                        }
                                    ],
                                },
                            }
                        },
                    },
                },
            }
        },
        "/Appointment/_search": {
            "post": {
                "tags": ["Type:Appointment"],
                "summary": "Appointment search-type",
                "description": "The Appointment search-type interaction searches a set of resources based on some filter criteria.",
                "operationId": "fhirstarter|type|search-type|post|Appointment|fhir.resources.appointment|Appointment",
                "requestBody": {
                    "content": {
                        "application/x-www-form-urlencoded": {
                            "schema": {
                                "properties": {
                                    "_format": {
                                        "type": "string",
                                        "title": " Format",
                                        "description": "Override the HTTP content negotiation to specify JSON or XML response format",
                                    },
                                    "_pretty": {
                                        "type": "string",
                                        "title": " Pretty",
                                        "description": "Ask for a pretty printed response for human convenience",
                                    },
                                },
                                "type": "object",
                                "title": "Body_fhirstarter|type|search-type|post|Appointment|fhir.resources.appointment|Appointment",
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Successful Appointment search-type",
                        "content": {
                            "application/fhir+json": {
                                "schema": {"$ref": "#/components/schemas/Bundle"},
                                "example": {
                                    "resourceType": "Bundle",
                                    "id": "bundle-example",
                                    "meta": {"lastUpdated": "2014-08-18T01:43:30Z"},
                                    "type": "searchset",
                                    "total": 3,
                                    "link": [
                                        {
                                            "relation": "self",
                                            "url": "https://example.com/base/Appointment?_count=1",
                                        },
                                        {
                                            "relation": "next",
                                            "url": "https://example.com/base/Appointment?searchId=ff15fd40-ff71-4b48-b366-09c706bed9d0&page=2",
                                        },
                                    ],
                                    "entry": [
                                        {
                                            "fullUrl": "https://example.com/base/Appointment/example",
                                            "resource": {
                                                "resourceType": "Appointment",
                                                "id": "example",
                                                "text": {
                                                    "status": "generated",
                                                    "div": '<div xmlns="http://www.w3.org/1999/xhtml">Brian MRI results discussion</div>',
                                                },
                                                "status": "booked",
                                                "class": [
                                                    {
                                                        "coding": [
                                                            {
                                                                "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
                                                                "code": "AMB",
                                                                "display": "ambulatory",
                                                            }
                                                        ]
                                                    }
                                                ],
                                                "serviceCategory": [
                                                    {
                                                        "coding": [
                                                            {
                                                                "system": "http://example.org/service-category",
                                                                "code": "gp",
                                                                "display": "General Practice",
                                                            }
                                                        ]
                                                    }
                                                ],
                                                "serviceType": [
                                                    {
                                                        "concept": {
                                                            "coding": [
                                                                {
                                                                    "code": "52",
                                                                    "display": "General Discussion",
                                                                }
                                                            ]
                                                        }
                                                    }
                                                ],
                                                "specialty": [
                                                    {
                                                        "coding": [
                                                            {
                                                                "system": "http://snomed.info/sct",
                                                                "code": "394814009",
                                                                "display": "General practice",
                                                            }
                                                        ]
                                                    }
                                                ],
                                                "appointmentType": {
                                                    "coding": [
                                                        {
                                                            "system": "http://terminology.hl7.org/CodeSystem/v2-0276",
                                                            "code": "FOLLOWUP",
                                                            "display": "A follow up visit from a previous appointment",
                                                        }
                                                    ]
                                                },
                                                "reason": [
                                                    {
                                                        "reference": {
                                                            "reference": "Condition/example",
                                                            "display": "Severe burn of left ear",
                                                        }
                                                    }
                                                ],
                                                "description": "Discussion on the results of your recent MRI",
                                                "start": "2013-12-10T09:00:00Z",
                                                "end": "2013-12-10T11:00:00Z",
                                                "created": "2013-10-10",
                                                "note": [
                                                    {
                                                        "text": "Further expand on the results of the MRI and determine the next actions that may be appropriate."
                                                    }
                                                ],
                                                "patientInstruction": [
                                                    {
                                                        "concept": {
                                                            "text": "Please avoid excessive travel (specifically flying) before this appointment"
                                                        }
                                                    }
                                                ],
                                                "basedOn": [
                                                    {
                                                        "reference": "ServiceRequest/myringotomy"
                                                    }
                                                ],
                                                "subject": {
                                                    "reference": "Patient/example",
                                                    "display": "Peter James Chalmers",
                                                },
                                                "participant": [
                                                    {
                                                        "actor": {
                                                            "reference": "Patient/example",
                                                            "display": "Peter James Chalmers",
                                                        },
                                                        "required": True,
                                                        "status": "accepted",
                                                    },
                                                    {
                                                        "type": [
                                                            {
                                                                "coding": [
                                                                    {
                                                                        "system": "http://terminology.hl7.org/CodeSystem/v3-ParticipationType",
                                                                        "code": "ATND",
                                                                    }
                                                                ]
                                                            }
                                                        ],
                                                        "actor": {
                                                            "reference": "Practitioner/example",
                                                            "display": "Dr Adam Careful",
                                                        },
                                                        "required": True,
                                                        "status": "accepted",
                                                    },
                                                    {
                                                        "actor": {
                                                            "reference": "Location/1",
                                                            "display": "South Wing, second floor",
                                                        },
                                                        "required": True,
                                                        "status": "accepted",
                                                    },
                                                ],
                                            },
                                            "search": {"mode": "match", "score": 1},
                                        }
                                    ],
                                },
                            }
                        },
                    },
                    "400": {
                        "description": "Appointment search-type request could not be parsed or failed basic FHIR validation rules.",
                        "content": {
                            "application/fhir+json": {
                                "schema": {
                                    "$ref": "#/components/schemas/OperationOutcome"
                                },
                                "example": {
                                    "resourceType": "OperationOutcome",
                                    "id": "101",
                                    "issue": [
                                        {
                                            "severity": "error",
                                            "code": "invalid",
                                            "details": {"text": "Bad request"},
                                        }
                                    ],
                                },
                            }
                        },
                    },
                    "401": {
                        "description": "Authentication is required for the Appointment search-type interaction that was attempted.",
                        "content": {
                            "application/fhir+json": {
                                "schema": {
                                    "$ref": "#/components/schemas/OperationOutcome"
                                },
                                "example": {
                                    "resourceType": "OperationOutcome",
                                    "id": "101",
                                    "issue": [
                                        {
                                            "severity": "error",
                                            "code": "unknown",
                                            "details": {
                                                "text": "Authentication failed"
                                            },
                                        }
                                    ],
                                },
                            }
                        },
                    },
                    "403": {
                        "description": "Authorization is required for the Appointment search-type interaction that was attempted.",
                        "content": {
                            "application/fhir+json": {
                                "schema": {
                                    "$ref": "#/components/schemas/OperationOutcome"
                                },
                                "example": {
                                    "resourceType": "OperationOutcome",
                                    "id": "101",
                                    "issue": [
                                        {
                                            "severity": "error",
                                            "code": "forbidden",
                                            "details": {"text": "Authorization failed"},
                                        }
                                    ],
                                },
                            }
                        },
                    },
                    "500": {
                        "description": "The server has encountered a situation it does not know how to handle.",
                        "content": {
                            "application/fhir+json": {
                                "schema": {
                                    "$ref": "#/components/schemas/OperationOutcome"
                                },
                                "example": {
                                    "resourceType": "OperationOutcome",
                                    "id": "101",
                                    "issue": [
                                        {
                                            "severity": "error",
                                            "code": "exception",
                                            "details": {
                                                "text": "Internal server error"
                                            },
                                        }
                                    ],
                                },
                            }
                        },
                    },
                },
            }
        },
        "/Practitioner/{id}": {
            "get": {
                "tags": ["Type:Practitioner"],
                "summary": "Practitioner read",
                "description": "The Practitioner read interaction accesses the current contents of a Practitioner resource.",
                "operationId": "fhirstarter|instance|read|get|Practitioner|fhir.resources.practitioner|Practitioner",
                "parameters": [
                    {
                        "description": "Logical id of this artifact",
                        "required": True,
                        "schema": {
                            "type": "string",
                            "maxLength": 64,
                            "minLength": 1,
                            "pattern": "^[A-Za-z0-9\\-.]+$",
                            "title": "Id",
                            "description": "Logical id of this artifact",
                        },
                        "name": "id",
                        "in": "path",
                    },
                    {
                        "description": "Override the HTTP content negotiation to specify JSON or XML response format",
                        "required": False,
                        "schema": {
                            "type": "string",
                            "title": " Format",
                            "description": "Override the HTTP content negotiation to specify JSON or XML response format",
                        },
                        "name": "_format",
                        "in": "query",
                    },
                    {
                        "description": "Ask for a pretty printed response for human convenience",
                        "required": False,
                        "schema": {
                            "type": "string",
                            "title": " Pretty",
                            "description": "Ask for a pretty printed response for human convenience",
                        },
                        "name": "_pretty",
                        "in": "query",
                    },
                ],
                "responses": {
                    "200": {
                        "description": "Successful Practitioner read",
                        "content": {
                            "application/fhir+json": {
                                "schema": {"$ref": "#/components/schemas/Practitioner"},
                                "examples": {
                                    "example": {
                                        "summary": "General Person Example",
                                        "description": "General Person Example",
                                        "value": {
                                            "resourceType": "Practitioner",
                                            "id": "example",
                                            "text": {
                                                "status": "generated",
                                                "div": '<div xmlns="http://www.w3.org/1999/xhtml">\n      <p>Dr Adam Careful is a Referring Practitioner for Acme Hospital from 1-Jan 2012 to 31-Mar\n        2012</p>\n    </div>',
                                            },
                                            "identifier": [
                                                {
                                                    "system": "http://www.acme.org/practitioners",
                                                    "value": "23",
                                                }
                                            ],
                                            "active": True,
                                            "name": [
                                                {
                                                    "family": "Careful",
                                                    "given": ["Adam"],
                                                    "prefix": ["Dr"],
                                                }
                                            ],
                                            "address": [
                                                {
                                                    "use": "home",
                                                    "line": ["534 Erewhon St"],
                                                    "city": "PleasantVille",
                                                    "state": "Vic",
                                                    "postalCode": "3999",
                                                }
                                            ],
                                            "qualification": [
                                                {
                                                    "identifier": [
                                                        {
                                                            "system": "http://example.org/UniversityIdentifier",
                                                            "value": "12345",
                                                        }
                                                    ],
                                                    "code": {
                                                        "coding": [
                                                            {
                                                                "system": "http://terminology.hl7.org/CodeSystem/v2-0360/2.7",
                                                                "code": "BS",
                                                                "display": "Bachelor of Science",
                                                            }
                                                        ],
                                                        "text": "Bachelor of Science",
                                                    },
                                                    "period": {"start": "1995"},
                                                    "issuer": {
                                                        "display": "Example University"
                                                    },
                                                }
                                            ],
                                        },
                                    },
                                    "xcda-author": {
                                        "summary": "CDA Example Author",
                                        "description": "CDA Example Author",
                                        "externalValue": "https://hl7.org/fhir/R5/practitioner-example-xcda-author.json",
                                    },
                                    "3ad0687e-f477-468c-afd5-fcc2bf897809": {
                                        "summary": "HL7 Defined Practitioner Examples",
                                        "description": "HL7 Defined Practitioner Examples",
                                        "externalValue": "https://hl7.org/fhir/R5/practitioner-examples-general.json",
                                    },
                                    "f001": {
                                        "summary": "Fictive KNO-physician",
                                        "description": "Fictive KNO-physician",
                                        "externalValue": "https://hl7.org/fhir/R5/practitioner-example-f001-evdb.json",
                                    },
                                    "f002": {
                                        "summary": "Fictive Cardiothoracal surgeon",
                                        "description": "Fictive Cardiothoracal surgeon",
                                        "externalValue": "https://hl7.org/fhir/R5/practitioner-example-f002-pv.json",
                                    },
                                    "f003": {
                                        "summary": "Fictive Cardiothoracal surgeon",
                                        "description": "Fictive Cardiothoracal surgeon",
                                        "externalValue": "https://hl7.org/fhir/R5/practitioner-example-f003-mv.json",
                                    },
                                    "f004": {
                                        "summary": "Fictive KNO-physician",
                                        "description": "Fictive KNO-physician",
                                        "externalValue": "https://hl7.org/fhir/R5/practitioner-example-f004-rb.json",
                                    },
                                    "f005": {
                                        "summary": "Fictive KNO-physician",
                                        "description": "Fictive KNO-physician",
                                        "externalValue": "https://hl7.org/fhir/R5/practitioner-example-f005-al.json",
                                    },
                                    "f201": {
                                        "summary": "Fictive Oncologist/Pulmonologist",
                                        "description": "Fictive Oncologist/Pulmonologist",
                                        "externalValue": "https://hl7.org/fhir/R5/practitioner-example-f201-ab.json",
                                    },
                                    "f202": {
                                        "summary": "Fictive Lab worker",
                                        "description": "Fictive Lab worker",
                                        "externalValue": "https://hl7.org/fhir/R5/practitioner-example-f202-lm.json",
                                    },
                                    "f203": {
                                        "summary": "Fictive Physiotherapist",
                                        "description": "Fictive Physiotherapist",
                                        "externalValue": "https://hl7.org/fhir/R5/practitioner-example-f203-jvg.json",
                                    },
                                    "f204": {
                                        "summary": "Fictive Nurse",
                                        "description": "Fictive Nurse",
                                        "externalValue": "https://hl7.org/fhir/R5/practitioner-example-f204-ce.json",
                                    },
                                    "f006": {
                                        "summary": "Fictive Pharmacist",
                                        "description": "Fictive Pharmacist",
                                        "externalValue": "https://hl7.org/fhir/R5/practitioner-example-f006-rvdb.json",
                                    },
                                    "f007": {
                                        "summary": "Fictive physician",
                                        "description": "Fictive physician",
                                        "externalValue": "https://hl7.org/fhir/R5/practitioner-example-f007-sh.json",
                                    },
                                    "xcda1": {
                                        "summary": "2nd CDA Example Author",
                                        "description": "2nd CDA Example Author",
                                        "externalValue": "https://hl7.org/fhir/R5/practitioner-example-xcda1.json",
                                    },
                                    "prac4": {
                                        "summary": "Deceased Practitioner (details also in person)",
                                        "description": "Deceased Practitioner (details also in person)",
                                        "externalValue": "https://hl7.org/fhir/R5/practitioner-example-prac4.json",
                                    },
                                },
                            }
                        },
                    },
                    "401": {
                        "description": "Authentication is required for the Practitioner read interaction that was attempted.",
                        "content": {
                            "application/fhir+json": {
                                "schema": {
                                    "$ref": "#/components/schemas/OperationOutcome"
                                },
                                "example": {
                                    "resourceType": "OperationOutcome",
                                    "id": "101",
                                    "issue": [
                                        {
                                            "severity": "error",
                                            "code": "unknown",
                                            "details": {
                                                "text": "Authentication failed"
                                            },
                                        }
                                    ],
                                },
                            }
                        },
                    },
                    "403": {
                        "description": "Authorization is required for the Practitioner read interaction that was attempted.",
                        "content": {
                            "application/fhir+json": {
                                "schema": {
                                    "$ref": "#/components/schemas/OperationOutcome"
                                },
                                "example": {
                                    "resourceType": "OperationOutcome",
                                    "id": "101",
                                    "issue": [
                                        {
                                            "severity": "error",
                                            "code": "forbidden",
                                            "details": {"text": "Authorization failed"},
                                        }
                                    ],
                                },
                            }
                        },
                    },
                    "404": {
                        "description": "Unknown Practitioner resource",
                        "content": {
                            "application/fhir+json": {
                                "schema": {
                                    "$ref": "#/components/schemas/OperationOutcome"
                                },
                                "example": {
                                    "resourceType": "OperationOutcome",
                                    "id": "101",
                                    "issue": [
                                        {
                                            "severity": "error",
                                            "code": "not-found",
                                            "details": {"text": "Resource not found"},
                                        }
                                    ],
                                },
                            }
                        },
                    },
                    "500": {
                        "description": "The server has encountered a situation it does not know how to handle.",
                        "content": {
                            "application/fhir+json": {
                                "schema": {
                                    "$ref": "#/components/schemas/OperationOutcome"
                                },
                                "example": {
                                    "resourceType": "OperationOutcome",
                                    "id": "101",
                                    "issue": [
                                        {
                                            "severity": "error",
                                            "code": "exception",
                                            "details": {
                                                "text": "Internal server error"
                                            },
                                        }
                                    ],
                                },
                            }
                        },
                    },
                },
            }
        },
        "/Practitioner": {
            "get": {
                "tags": ["Type:Practitioner"],
                "summary": "Practitioner search-type",
                "description": "The Practitioner search-type interaction searches a set of resources based on some filter criteria.",
                "operationId": "fhirstarter|type|search-type|get|Practitioner|fhirstarter.tests.test_openapi|PractitionerCustom",
                "parameters": [
                    {
                        "description": "Override the HTTP content negotiation to specify JSON or XML response format",
                        "required": False,
                        "schema": {
                            "type": "string",
                            "title": " Format",
                            "description": "Override the HTTP content negotiation to specify JSON or XML response format",
                        },
                        "name": "_format",
                        "in": "query",
                    },
                    {
                        "description": "Ask for a pretty printed response for human convenience",
                        "required": False,
                        "schema": {
                            "type": "string",
                            "title": " Pretty",
                            "description": "Ask for a pretty printed response for human convenience",
                        },
                        "name": "_pretty",
                        "in": "query",
                    },
                ],
                "responses": {
                    "200": {
                        "description": "Successful Practitioner search-type",
                        "content": {
                            "application/fhir+json": {
                                "schema": {"$ref": "#/components/schemas/Bundle"},
                                "example": {
                                    "resourceType": "Bundle",
                                    "id": "bundle-example",
                                    "meta": {"lastUpdated": "2014-08-18T01:43:30Z"},
                                    "type": "searchset",
                                    "total": 3,
                                    "link": [
                                        {
                                            "relation": "self",
                                            "url": "https://example.com/base/Practitioner?_count=1",
                                        },
                                        {
                                            "relation": "next",
                                            "url": "https://example.com/base/Practitioner?searchId=ff15fd40-ff71-4b48-b366-09c706bed9d0&page=2",
                                        },
                                    ],
                                    "entry": [
                                        {
                                            "fullUrl": "https://example.com/base/Practitioner/example",
                                            "resource": {
                                                "resourceType": "Practitioner",
                                                "id": "example",
                                                "name": [
                                                    {
                                                        "family": "Careful",
                                                        "given": ["Adam"],
                                                        "prefix": ["Dr"],
                                                    }
                                                ],
                                            },
                                            "search": {"mode": "match", "score": 1},
                                        }
                                    ],
                                },
                            }
                        },
                    },
                    "400": {
                        "description": "Practitioner search-type request could not be parsed or failed basic FHIR validation rules.",
                        "content": {
                            "application/fhir+json": {
                                "schema": {
                                    "$ref": "#/components/schemas/OperationOutcome"
                                },
                                "example": {
                                    "resourceType": "OperationOutcome",
                                    "id": "101",
                                    "issue": [
                                        {
                                            "severity": "error",
                                            "code": "invalid",
                                            "details": {"text": "Bad request"},
                                        }
                                    ],
                                },
                            }
                        },
                    },
                    "401": {
                        "description": "Authentication is required for the Practitioner search-type interaction that was attempted.",
                        "content": {
                            "application/fhir+json": {
                                "schema": {
                                    "$ref": "#/components/schemas/OperationOutcome"
                                },
                                "example": {
                                    "resourceType": "OperationOutcome",
                                    "id": "101",
                                    "issue": [
                                        {
                                            "severity": "error",
                                            "code": "unknown",
                                            "details": {
                                                "text": "Authentication failed"
                                            },
                                        }
                                    ],
                                },
                            }
                        },
                    },
                    "403": {
                        "description": "Authorization is required for the Practitioner search-type interaction that was attempted.",
                        "content": {
                            "application/fhir+json": {
                                "schema": {
                                    "$ref": "#/components/schemas/OperationOutcome"
                                },
                                "example": {
                                    "resourceType": "OperationOutcome",
                                    "id": "101",
                                    "issue": [
                                        {
                                            "severity": "error",
                                            "code": "forbidden",
                                            "details": {"text": "Authorization failed"},
                                        }
                                    ],
                                },
                            }
                        },
                    },
                    "500": {
                        "description": "The server has encountered a situation it does not know how to handle.",
                        "content": {
                            "application/fhir+json": {
                                "schema": {
                                    "$ref": "#/components/schemas/OperationOutcome"
                                },
                                "example": {
                                    "resourceType": "OperationOutcome",
                                    "id": "101",
                                    "issue": [
                                        {
                                            "severity": "error",
                                            "code": "exception",
                                            "details": {
                                                "text": "Internal server error"
                                            },
                                        }
                                    ],
                                },
                            }
                        },
                    },
                },
            }
        },
        "/Practitioner/_search": {
            "post": {
                "tags": ["Type:Practitioner"],
                "summary": "Practitioner search-type",
                "description": "The Practitioner search-type interaction searches a set of resources based on some filter criteria.",
                "operationId": "fhirstarter|type|search-type|post|Practitioner|fhirstarter.tests.test_openapi|PractitionerCustom",
                "requestBody": {
                    "content": {
                        "application/x-www-form-urlencoded": {
                            "schema": {
                                "properties": {
                                    "_format": {
                                        "type": "string",
                                        "title": " Format",
                                        "description": "Override the HTTP content negotiation to specify JSON or XML response format",
                                    },
                                    "_pretty": {
                                        "type": "string",
                                        "title": " Pretty",
                                        "description": "Ask for a pretty printed response for human convenience",
                                    },
                                },
                                "type": "object",
                                "title": "Body_fhirstarter|type|search-type|post|Practitioner|fhirstarter.tests.test_openapi|PractitionerCustom",
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Successful Practitioner search-type",
                        "content": {
                            "application/fhir+json": {
                                "schema": {"$ref": "#/components/schemas/Bundle"},
                                "example": {
                                    "resourceType": "Bundle",
                                    "id": "bundle-example",
                                    "meta": {"lastUpdated": "2014-08-18T01:43:30Z"},
                                    "type": "searchset",
                                    "total": 3,
                                    "link": [
                                        {
                                            "relation": "self",
                                            "url": "https://example.com/base/Practitioner?_count=1",
                                        },
                                        {
                                            "relation": "next",
                                            "url": "https://example.com/base/Practitioner?searchId=ff15fd40-ff71-4b48-b366-09c706bed9d0&page=2",
                                        },
                                    ],
                                    "entry": [
                                        {
                                            "fullUrl": "https://example.com/base/Practitioner/example",
                                            "resource": {
                                                "resourceType": "Practitioner",
                                                "id": "example",
                                                "name": [
                                                    {
                                                        "family": "Careful",
                                                        "given": ["Adam"],
                                                        "prefix": ["Dr"],
                                                    }
                                                ],
                                            },
                                            "search": {"mode": "match", "score": 1},
                                        }
                                    ],
                                },
                            }
                        },
                    },
                    "400": {
                        "description": "Practitioner search-type request could not be parsed or failed basic FHIR validation rules.",
                        "content": {
                            "application/fhir+json": {
                                "schema": {
                                    "$ref": "#/components/schemas/OperationOutcome"
                                },
                                "example": {
                                    "resourceType": "OperationOutcome",
                                    "id": "101",
                                    "issue": [
                                        {
                                            "severity": "error",
                                            "code": "invalid",
                                            "details": {"text": "Bad request"},
                                        }
                                    ],
                                },
                            }
                        },
                    },
                    "401": {
                        "description": "Authentication is required for the Practitioner search-type interaction that was attempted.",
                        "content": {
                            "application/fhir+json": {
                                "schema": {
                                    "$ref": "#/components/schemas/OperationOutcome"
                                },
                                "example": {
                                    "resourceType": "OperationOutcome",
                                    "id": "101",
                                    "issue": [
                                        {
                                            "severity": "error",
                                            "code": "unknown",
                                            "details": {
                                                "text": "Authentication failed"
                                            },
                                        }
                                    ],
                                },
                            }
                        },
                    },
                    "403": {
                        "description": "Authorization is required for the Practitioner search-type interaction that was attempted.",
                        "content": {
                            "application/fhir+json": {
                                "schema": {
                                    "$ref": "#/components/schemas/OperationOutcome"
                                },
                                "example": {
                                    "resourceType": "OperationOutcome",
                                    "id": "101",
                                    "issue": [
                                        {
                                            "severity": "error",
                                            "code": "forbidden",
                                            "details": {"text": "Authorization failed"},
                                        }
                                    ],
                                },
                            }
                        },
                    },
                    "500": {
                        "description": "The server has encountered a situation it does not know how to handle.",
                        "content": {
                            "application/fhir+json": {
                                "schema": {
                                    "$ref": "#/components/schemas/OperationOutcome"
                                },
                                "example": {
                                    "resourceType": "OperationOutcome",
                                    "id": "101",
                                    "issue": [
                                        {
                                            "severity": "error",
                                            "code": "exception",
                                            "details": {
                                                "text": "Internal server error"
                                            },
                                        }
                                    ],
                                },
                            }
                        },
                    },
                },
            }
        },
    },
    "components": {
        "schemas": {
            "Appointment": {
                "title": "Appointment",
                "description": "Disclaimer: Any field name ends with ``__ext`` doesn't part of\nResource StructureDefinition, instead used to enable Extensibility feature\nfor FHIR Primitive Data Types.\n\nA booking of a healthcare event among patient(s), practitioner(s), related\nperson(s) and/or device(s) for a specific date/time. This may result in one\nor more Encounter(s).",
                "type": "object",
                "properties": {
                    "resource_type": {
                        "title": "Resource Type",
                        "default": "Appointment",
                        "const": "Appointment",
                        "type": "string",
                    },
                    "fhir_comments": {
                        "title": "Fhir Comments",
                        "element_property": False,
                        "anyOf": [
                            {"type": "string"},
                            {"type": "array", "items": {"type": "string"}},
                        ],
                    },
                    "id": {
                        "title": "Logical id of this artifact",
                        "description": "The logical id of the resource, as used in the URL for the resource. Once assigned, this value never changes.",
                        "element_property": True,
                        "minLength": 1,
                        "maxLength": 64,
                        "pattern": "^[A-Za-z0-9\\-.]+$",
                        "type": "string",
                    },
                    "implicitRules": {
                        "title": "A set of rules under which this content was created",
                        "description": "A reference to a set of rules that were followed when the resource was constructed, and which must be understood when processing the content. Often, this is a reference to an implementation guide that defines the special rules along with other profiles etc.",
                        "element_property": True,
                        "pattern": "\\S*",
                        "type": "string",
                    },
                    "_implicitRules": {
                        "title": "Extension field for ``implicitRules``.",
                        "type": "FHIRPrimitiveExtension",
                    },
                    "language": {
                        "title": "Language of the resource content",
                        "description": "The base language in which the resource is written.",
                        "element_property": True,
                        "pattern": "^[^\\s]+(\\s[^\\s]+)*$",
                        "type": "string",
                    },
                    "_language": {
                        "title": "Extension field for ``language``.",
                        "type": "FHIRPrimitiveExtension",
                    },
                    "meta": {
                        "title": "Metadata about the resource",
                        "description": "The metadata about the resource. This is content that is maintained by the infrastructure. Changes to the content might not always be associated with version changes to the resource.",
                        "element_property": True,
                        "type": "Meta",
                    },
                    "contained": {
                        "title": "Contained, inline Resources",
                        "description": "These resources do not have an independent existence apart from the resource that contains them - they cannot be identified independently, nor can they have their own independent transaction scope. This is allowed to be a Parameters resource if and only if it is referenced by a resource that provides context/meaning.",
                        "element_property": True,
                        "type": "array",
                        "items": {"type": "Resource"},
                    },
                    "extension": {
                        "title": "Additional content defined by implementations",
                        "description": "May be used to represent additional information that is not part of the basic definition of the resource. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
                        "element_property": True,
                        "type": "array",
                        "items": {"type": "Extension"},
                    },
                    "modifierExtension": {
                        "title": "Extensions that cannot be ignored",
                        "description": "May be used to represent additional information that is not part of the basic definition of the resource and that modifies the understanding of the element that contains it and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer is allowed to define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions.  Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
                        "element_property": True,
                        "type": "array",
                        "items": {"type": "Extension"},
                    },
                    "text": {
                        "title": "Text summary of the resource, for human interpretation",
                        "description": 'A human-readable narrative that contains a summary of the resource and can be used to represent the content of the resource to a human. The narrative need not encode all the structured data, but is required to contain sufficient detail to make it "clinically safe" for a human to just read the narrative. Resource definitions may define what content should be represented in the narrative to ensure clinical safety.',
                        "element_property": True,
                        "type": "Narrative",
                    },
                    "account": {
                        "title": "The set of accounts that may be used for billing for this Appointment",
                        "description": "The set of accounts that is expected to be used for billing the activities that result from this Appointment.",
                        "element_property": True,
                        "enum_reference_types": ["Account"],
                        "type": "array",
                        "items": {"type": "Reference"},
                    },
                    "appointmentType": {
                        "title": "The style of appointment or patient that has been booked in the slot (not service type)",
                        "element_property": True,
                        "type": "CodeableConcept",
                    },
                    "basedOn": {
                        "title": "The request this appointment is allocated to assess",
                        "description": "The request this appointment is allocated to assess (e.g. incoming referral or procedure request).",
                        "element_property": True,
                        "enum_reference_types": [
                            "CarePlan",
                            "DeviceRequest",
                            "MedicationRequest",
                            "ServiceRequest",
                        ],
                        "type": "array",
                        "items": {"type": "Reference"},
                    },
                    "cancellationDate": {
                        "title": "When the appointment was cancelled",
                        "description": "The date/time describing when the appointment was cancelled.",
                        "element_property": True,
                        "type": "string",
                        "format": "date-time",
                    },
                    "_cancellationDate": {
                        "title": "Extension field for ``cancellationDate``.",
                        "type": "FHIRPrimitiveExtension",
                    },
                    "cancellationReason": {
                        "title": "The coded reason for the appointment being cancelled",
                        "description": "The coded reason for the appointment being cancelled. This is often used in reporting/billing/futher processing to determine if further actions are required, or specific fees apply.",
                        "element_property": True,
                        "type": "CodeableConcept",
                    },
                    "class": {
                        "title": "Classification when becoming an encounter",
                        "description": "Concepts representing classification of patient encounter such as ambulatory (outpatient), inpatient, emergency, home health or others due to local variations.",
                        "element_property": True,
                        "type": "array",
                        "items": {"type": "CodeableConcept"},
                    },
                    "created": {
                        "title": "The date that this appointment was initially created",
                        "description": "The date that this appointment was initially created. This could be different to the meta.lastModified value on the initial entry, as this could have been before the resource was created on the FHIR server, and should remain unchanged over the lifespan of the appointment.",
                        "element_property": True,
                        "type": "string",
                        "format": "date-time",
                    },
                    "_created": {
                        "title": "Extension field for ``created``.",
                        "type": "FHIRPrimitiveExtension",
                    },
                    "description": {
                        "title": "Shown on a subject line in a meeting request, or appointment list",
                        "description": "The brief description of the appointment as would be shown on a subject line in a meeting request, or appointment list. Detailed or expanded information should be put in the note field.",
                        "element_property": True,
                        "pattern": "[ \\r\\n\\t\\S]+",
                        "type": "string",
                    },
                    "_description": {
                        "title": "Extension field for ``description``.",
                        "type": "FHIRPrimitiveExtension",
                    },
                    "end": {
                        "title": "When appointment is to conclude",
                        "description": "Date/Time that the appointment is to conclude.",
                        "element_property": True,
                        "type": "string",
                        "format": "date-time",
                    },
                    "_end": {
                        "title": "Extension field for ``end``.",
                        "type": "FHIRPrimitiveExtension",
                    },
                    "identifier": {
                        "title": "External Ids for this item",
                        "description": "This records identifiers associated with this appointment concern that are defined by business processes and/or used to refer to it when a direct URL reference to the resource itself is not appropriate (e.g. in CDA documents, or in written / printed documentation).",
                        "element_property": True,
                        "type": "array",
                        "items": {"type": "Identifier"},
                    },
                    "minutesDuration": {
                        "title": "Can be less than start/end (e.g. estimate)",
                        "description": "Number of minutes that the appointment is to take. This can be less than the duration between the start and end times.  For example, where the actual time of appointment is only an estimate or if a 30 minute appointment is being requested, but any time would work.  Also, if there is, for example, a planned 15 minute break in the middle of a long appointment, the duration may be 15 minutes less than the difference between the start and end.",
                        "element_property": True,
                        "exclusiveMinimum": 0,
                        "type": "integer",
                    },
                    "_minutesDuration": {
                        "title": "Extension field for ``minutesDuration``.",
                        "type": "FHIRPrimitiveExtension",
                    },
                    "note": {
                        "title": "Additional comments",
                        "description": "Additional notes/comments about the appointment.",
                        "element_property": True,
                        "type": "array",
                        "items": {"type": "Annotation"},
                    },
                    "occurrenceChanged": {
                        "title": "Indicates that this appointment varies from a recurrence pattern",
                        "description": "This appointment varies from the recurring pattern.",
                        "element_property": True,
                        "type": "boolean",
                    },
                    "_occurrenceChanged": {
                        "title": "Extension field for ``occurrenceChanged``.",
                        "type": "FHIRPrimitiveExtension",
                    },
                    "originatingAppointment": {
                        "title": "The originating appointment in a recurring set of appointments",
                        "description": "The originating appointment in a recurring set of related appointments.",
                        "element_property": True,
                        "enum_reference_types": ["Appointment"],
                        "type": "Reference",
                    },
                    "participant": {
                        "title": "Participants involved in appointment",
                        "description": "List of participants involved in the appointment.",
                        "element_property": True,
                        "type": "array",
                        "items": {"type": "AppointmentParticipant"},
                    },
                    "patientInstruction": {
                        "title": "Detailed information and instructions for the patient",
                        "description": "While Appointment.note contains information for internal use, Appointment.patientInstructions is used to capture patient facing information about the Appointment (e.g. please bring your referral or fast from 8pm night before).",
                        "element_property": True,
                        "enum_reference_types": [
                            "DocumentReference",
                            "Binary",
                            "Communication",
                        ],
                        "type": "array",
                        "items": {"type": "CodeableReference"},
                    },
                    "previousAppointment": {
                        "title": "The previous appointment in a series",
                        "description": "The previous appointment in a series of related appointments.",
                        "element_property": True,
                        "enum_reference_types": ["Appointment"],
                        "type": "Reference",
                    },
                    "priority": {
                        "title": "Used to make informed decisions if needing to re-prioritize",
                        "description": "The priority of the appointment. Can be used to make informed decisions if needing to re-prioritize appointments. (The iCal Standard specifies 0 as undefined, 1 as highest, 9 as lowest priority).",
                        "element_property": True,
                        "type": "CodeableConcept",
                    },
                    "reason": {
                        "title": "Reason this appointment is scheduled",
                        "description": "The reason that this appointment is being scheduled. This is more clinical than administrative. This can be coded, or as specified using information from another resource. When the patient arrives and the encounter begins it may be used as the admission diagnosis. The indication will typically be a Condition (with other resources referenced in the evidence.detail), or a Procedure.",
                        "element_property": True,
                        "enum_reference_types": [
                            "Condition",
                            "Procedure",
                            "Observation",
                            "ImmunizationRecommendation",
                        ],
                        "type": "array",
                        "items": {"type": "CodeableReference"},
                    },
                    "recurrenceId": {
                        "title": "The sequence number in the recurrence",
                        "description": "The sequence number that identifies a specific appointment in a recurring pattern.",
                        "element_property": True,
                        "exclusiveMinimum": 0,
                        "type": "integer",
                    },
                    "_recurrenceId": {
                        "title": "Extension field for ``recurrenceId``.",
                        "type": "FHIRPrimitiveExtension",
                    },
                    "recurrenceTemplate": {
                        "title": "Details of the recurrence pattern/template used to generate occurrences",
                        "description": "The details of the recurrence pattern or template that is used to generate recurring appointments.",
                        "element_property": True,
                        "type": "array",
                        "items": {"type": "AppointmentRecurrenceTemplate"},
                    },
                    "replaces": {
                        "title": "Appointment replaced by this Appointment",
                        "description": "Appointment replaced by this Appointment in cases where there is a cancellation, the details of the cancellation can be found in the cancellationReason property (on the referenced resource).",
                        "element_property": True,
                        "enum_reference_types": ["Appointment"],
                        "type": "array",
                        "items": {"type": "Reference"},
                    },
                    "requestedPeriod": {
                        "title": "Potential date/time interval(s) requested to allocate the appointment within",
                        "description": "A set of date ranges (potentially including times) that the appointment is preferred to be scheduled within.  The duration (usually in minutes) could also be provided to indicate the length of the appointment to fill and populate the start/end times for the actual allocated time. However, in other situations the duration may be calculated by the scheduling system.",
                        "element_property": True,
                        "type": "array",
                        "items": {"type": "Period"},
                    },
                    "serviceCategory": {
                        "title": "A broad categorization of the service that is to be performed during this appointment",
                        "element_property": True,
                        "type": "array",
                        "items": {"type": "CodeableConcept"},
                    },
                    "serviceType": {
                        "title": "The specific service that is to be performed during this appointment",
                        "element_property": True,
                        "enum_reference_types": ["HealthcareService"],
                        "type": "array",
                        "items": {"type": "CodeableReference"},
                    },
                    "slot": {
                        "title": "The slots that this appointment is filling",
                        "description": "The slots from the participants' schedules that will be filled by the appointment.",
                        "element_property": True,
                        "enum_reference_types": ["Slot"],
                        "type": "array",
                        "items": {"type": "Reference"},
                    },
                    "specialty": {
                        "title": "The specialty of a practitioner that would be required to perform the service requested in this appointment",
                        "element_property": True,
                        "type": "array",
                        "items": {"type": "CodeableConcept"},
                    },
                    "start": {
                        "title": "When appointment is to take place",
                        "description": "Date/Time that the appointment is to take place.",
                        "element_property": True,
                        "type": "string",
                        "format": "date-time",
                    },
                    "_start": {
                        "title": "Extension field for ``start``.",
                        "type": "FHIRPrimitiveExtension",
                    },
                    "status": {
                        "title": "proposed | pending | booked | arrived | fulfilled | cancelled | noshow | entered-in-error | checked-in | waitlist",
                        "description": "The overall status of the Appointment. Each of the participants has their own participation status which indicates their involvement in the process, however this status indicates the shared status.",
                        "element_property": True,
                        "element_required": True,
                        "enum_values": [
                            "proposed",
                            "pending",
                            "booked",
                            "arrived",
                            "fulfilled",
                            "cancelled",
                            "noshow",
                            "entered-in-error",
                            "checked-in",
                            "waitlist",
                        ],
                        "pattern": "^[^\\s]+(\\s[^\\s]+)*$",
                        "type": "string",
                    },
                    "_status": {
                        "title": "Extension field for ``status``.",
                        "type": "FHIRPrimitiveExtension",
                    },
                    "subject": {
                        "title": "The patient or group associated with the appointment",
                        "description": "The patient or group associated with the appointment, if they are to be present (usually) then they should also be included in the participant backbone element.",
                        "element_property": True,
                        "enum_reference_types": ["Patient", "Group"],
                        "type": "Reference",
                    },
                    "supportingInformation": {
                        "title": "Additional information to support the appointment",
                        "description": "Additional information to support the appointment provided when making the appointment.",
                        "element_property": True,
                        "enum_reference_types": ["Resource"],
                        "type": "array",
                        "items": {"type": "Reference"},
                    },
                    "virtualService": {
                        "title": "Connection details of a virtual service (e.g. conference call)",
                        "element_property": True,
                        "type": "array",
                        "items": {"type": "VirtualServiceDetail"},
                    },
                },
                "required": ["participant"],
                "additionalProperties": False,
            },
            "Bundle": {
                "properties": {
                    "resource_type": {
                        "type": "string",
                        "const": "Bundle",
                        "title": "Resource Type",
                        "default": "Bundle",
                    },
                    "fhir_comments": {
                        "anyOf": [
                            {"type": "string"},
                            {"items": {"type": "string"}, "type": "array"},
                        ],
                        "title": "Fhir Comments",
                        "element_property": False,
                    },
                    "id": {
                        "type": "string",
                        "maxLength": 64,
                        "minLength": 1,
                        "pattern": "^[A-Za-z0-9\\-.]+$",
                        "title": "Logical id of this artifact",
                        "description": "The logical id of the resource, as used in the URL for the resource. Once assigned, this value never changes.",
                        "element_property": True,
                    },
                    "implicitRules": {
                        "type": "string",
                        "pattern": "\\S*",
                        "title": "A set of rules under which this content was created",
                        "description": "A reference to a set of rules that were followed when the resource was constructed, and which must be understood when processing the content. Often, this is a reference to an implementation guide that defines the special rules along with other profiles etc.",
                        "element_property": True,
                    },
                    "_implicitRules": {
                        "type": "FHIRPrimitiveExtension",
                        "title": "Extension field for ``implicitRules``.",
                    },
                    "language": {
                        "type": "string",
                        "pattern": "^[^\\s]+(\\s[^\\s]+)*$",
                        "title": "Language of the resource content",
                        "description": "The base language in which the resource is written.",
                        "element_property": True,
                    },
                    "_language": {
                        "type": "FHIRPrimitiveExtension",
                        "title": "Extension field for ``language``.",
                    },
                    "meta": {
                        "type": "Meta",
                        "title": "Metadata about the resource",
                        "description": "The metadata about the resource. This is content that is maintained by the infrastructure. Changes to the content might not always be associated with version changes to the resource.",
                        "element_property": True,
                    },
                    "entry": {
                        "items": {"type": "BundleEntry"},
                        "type": "array",
                        "title": "Entry in the bundle - will have a resource or information",
                        "description": "An entry in a bundle resource - will either contain a resource or information about a resource (transactions and history only).",
                        "element_property": True,
                    },
                    "identifier": {
                        "type": "Identifier",
                        "title": "Persistent identifier for the bundle",
                        "description": "A persistent identifier for the bundle that won't change as a bundle is copied from server to server.",
                        "element_property": True,
                    },
                    "issues": {
                        "type": "Resource",
                        "title": "Issues with the Bundle",
                        "description": "Captures issues and warnings that relate to the construction of the Bundle and the content within it.",
                        "element_property": True,
                    },
                    "link": {
                        "items": {"type": "BundleLink"},
                        "type": "array",
                        "title": "Links related to this Bundle",
                        "description": "A series of links that provide context to this bundle.",
                        "element_property": True,
                    },
                    "signature": {
                        "type": "Signature",
                        "title": "Digital Signature",
                        "description": "Digital Signature - base64 encoded. XML-DSig or a JWS.",
                        "element_property": True,
                    },
                    "timestamp": {
                        "type": "string",
                        "format": "date-time",
                        "title": "When the bundle was assembled",
                        "description": "The date/time that the bundle was assembled - i.e. when the resources were placed in the bundle.",
                        "element_property": True,
                    },
                    "_timestamp": {
                        "type": "FHIRPrimitiveExtension",
                        "title": "Extension field for ``timestamp``.",
                    },
                    "total": {
                        "type": "integer",
                        "minimum": 0.0,
                        "title": "If search, the total number of matches",
                        "description": "If a set of search matches, this is the (potentially estimated) total number of entries of type 'match' across all pages in the search.  It does not include search.mode = 'include' or 'outcome' entries and it does not provide a count of the number of entries in the Bundle.",
                        "element_property": True,
                    },
                    "_total": {
                        "type": "FHIRPrimitiveExtension",
                        "title": "Extension field for ``total``.",
                    },
                    "type": {
                        "type": "string",
                        "pattern": "^[^\\s]+(\\s[^\\s]+)*$",
                        "title": "document | message | transaction | transaction-response | batch | batch-response | history | searchset | collection | subscription-notification",
                        "description": "Indicates the purpose of this bundle - how it is intended to be used.",
                        "element_required": True,
                        "enum_values": [
                            "document",
                            "message",
                            "transaction",
                            "transaction-response",
                            "batch",
                            "batch-response",
                            "history",
                            "searchset",
                            "collection",
                            "subscription-notification",
                        ],
                        "element_property": True,
                    },
                    "_type": {
                        "type": "FHIRPrimitiveExtension",
                        "title": "Extension field for ``type``.",
                    },
                },
                "additionalProperties": False,
                "type": "object",
                "title": "Bundle",
                "description": "Disclaimer: Any field name ends with ``__ext`` doesn't part of\nResource StructureDefinition, instead used to enable Extensibility feature\nfor FHIR Primitive Data Types.\n\nContains a collection of resources.\nA container for a collection of resources.",
            },
            "CapabilityStatement": {
                "properties": {
                    "resource_type": {
                        "type": "string",
                        "const": "CapabilityStatement",
                        "title": "Resource Type",
                        "default": "CapabilityStatement",
                    },
                    "fhir_comments": {
                        "anyOf": [
                            {"type": "string"},
                            {"items": {"type": "string"}, "type": "array"},
                        ],
                        "title": "Fhir Comments",
                        "element_property": False,
                    },
                    "id": {
                        "type": "string",
                        "maxLength": 64,
                        "minLength": 1,
                        "pattern": "^[A-Za-z0-9\\-.]+$",
                        "title": "Logical id of this artifact",
                        "description": "The logical id of the resource, as used in the URL for the resource. Once assigned, this value never changes.",
                        "element_property": True,
                    },
                    "implicitRules": {
                        "type": "string",
                        "pattern": "\\S*",
                        "title": "A set of rules under which this content was created",
                        "description": "A reference to a set of rules that were followed when the resource was constructed, and which must be understood when processing the content. Often, this is a reference to an implementation guide that defines the special rules along with other profiles etc.",
                        "element_property": True,
                    },
                    "_implicitRules": {
                        "type": "FHIRPrimitiveExtension",
                        "title": "Extension field for ``implicitRules``.",
                    },
                    "language": {
                        "type": "string",
                        "pattern": "^[^\\s]+(\\s[^\\s]+)*$",
                        "title": "Language of the resource content",
                        "description": "The base language in which the resource is written.",
                        "element_property": True,
                    },
                    "_language": {
                        "type": "FHIRPrimitiveExtension",
                        "title": "Extension field for ``language``.",
                    },
                    "meta": {
                        "type": "Meta",
                        "title": "Metadata about the resource",
                        "description": "The metadata about the resource. This is content that is maintained by the infrastructure. Changes to the content might not always be associated with version changes to the resource.",
                        "element_property": True,
                    },
                    "contained": {
                        "items": {"type": "Resource"},
                        "type": "array",
                        "title": "Contained, inline Resources",
                        "description": "These resources do not have an independent existence apart from the resource that contains them - they cannot be identified independently, nor can they have their own independent transaction scope. This is allowed to be a Parameters resource if and only if it is referenced by a resource that provides context/meaning.",
                        "element_property": True,
                    },
                    "extension": {
                        "items": {"type": "Extension"},
                        "type": "array",
                        "title": "Additional content defined by implementations",
                        "description": "May be used to represent additional information that is not part of the basic definition of the resource. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
                        "element_property": True,
                    },
                    "modifierExtension": {
                        "items": {"type": "Extension"},
                        "type": "array",
                        "title": "Extensions that cannot be ignored",
                        "description": "May be used to represent additional information that is not part of the basic definition of the resource and that modifies the understanding of the element that contains it and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer is allowed to define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions.  Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
                        "element_property": True,
                    },
                    "text": {
                        "type": "Narrative",
                        "title": "Text summary of the resource, for human interpretation",
                        "description": 'A human-readable narrative that contains a summary of the resource and can be used to represent the content of the resource to a human. The narrative need not encode all the structured data, but is required to contain sufficient detail to make it "clinically safe" for a human to just read the narrative. Resource definitions may define what content should be represented in the narrative to ensure clinical safety.',
                        "element_property": True,
                    },
                    "acceptLanguage": {
                        "items": {
                            "type": "string",
                            "pattern": "^[^\\s]+(\\s[^\\s]+)*$",
                        },
                        "type": "array",
                        "title": "Languages supported",
                        "description": "A list of the languages supported by this implementation that are usefully supported in the ```Accept-Language``` header.",
                        "element_property": True,
                    },
                    "_acceptLanguage": {
                        "items": {"type": "FHIRPrimitiveExtension"},
                        "type": "array",
                        "title": "Extension field for ``acceptLanguage``.",
                    },
                    "contact": {
                        "items": {"type": "ContactDetail"},
                        "type": "array",
                        "title": "Contact details for the publisher",
                        "description": "Contact details to assist a user in finding and communicating with the publisher.",
                        "element_property": True,
                    },
                    "copyright": {
                        "type": "string",
                        "pattern": "\\s*(\\S|\\s)*",
                        "title": "Use and/or publishing restrictions",
                        "description": "A copyright statement relating to the capability statement and/or its contents. Copyright statements are generally legal restrictions on the use and publishing of the capability statement.",
                        "element_property": True,
                    },
                    "_copyright": {
                        "type": "FHIRPrimitiveExtension",
                        "title": "Extension field for ``copyright``.",
                    },
                    "copyrightLabel": {
                        "type": "string",
                        "pattern": "[ \\r\\n\\t\\S]+",
                        "title": "Copyright holder and year(s)",
                        "description": "A short string (<50 characters), suitable for inclusion in a page footer that identifies the copyright holder, effective period, and optionally whether rights are resctricted. (e.g. 'All rights reserved', 'Some rights reserved').",
                        "element_property": True,
                    },
                    "_copyrightLabel": {
                        "type": "FHIRPrimitiveExtension",
                        "title": "Extension field for ``copyrightLabel``.",
                    },
                    "date": {
                        "type": "string",
                        "format": "date-time",
                        "title": "Date last changed",
                        "description": "The date  (and optionally time) when the capability statement was last significantly changed. The date must change when the business version changes and it must change if the status code changes. In addition, it should change when the substantive content of the capability statement changes.",
                        "element_required": True,
                        "element_property": True,
                    },
                    "_date": {
                        "type": "FHIRPrimitiveExtension",
                        "title": "Extension field for ``date``.",
                    },
                    "description": {
                        "type": "string",
                        "pattern": "\\s*(\\S|\\s)*",
                        "title": "Natural language description of the capability statement",
                        "description": "A free text natural language description of the capability statement from a consumer's perspective. Typically, this is used when the capability statement describes a desired rather than an actual solution, for example as a formal expression of requirements as part of an RFP.",
                        "element_property": True,
                    },
                    "_description": {
                        "type": "FHIRPrimitiveExtension",
                        "title": "Extension field for ``description``.",
                    },
                    "document": {
                        "items": {"type": "CapabilityStatementDocument"},
                        "type": "array",
                        "title": "Document definition",
                        "description": "A document definition.",
                        "element_property": True,
                    },
                    "experimental": {
                        "type": "boolean",
                        "title": "For testing purposes, not real usage",
                        "description": "A Boolean value to indicate that this capability statement is authored for testing purposes (or education/evaluation/marketing) and is not intended to be used for genuine usage.",
                        "element_property": True,
                    },
                    "_experimental": {
                        "type": "FHIRPrimitiveExtension",
                        "title": "Extension field for ``experimental``.",
                    },
                    "fhirVersion": {
                        "type": "string",
                        "pattern": "^[^\\s]+(\\s[^\\s]+)*$",
                        "title": "FHIR Version the system supports",
                        "description": "The version of the FHIR specification that this CapabilityStatement describes (which SHALL be the same as the FHIR version of the CapabilityStatement itself). There is no default value.",
                        "element_required": True,
                        "element_property": True,
                    },
                    "_fhirVersion": {
                        "type": "FHIRPrimitiveExtension",
                        "title": "Extension field for ``fhirVersion``.",
                    },
                    "format": {
                        "items": {
                            "type": "string",
                            "pattern": "^[^\\s]+(\\s[^\\s]+)*$",
                        },
                        "type": "array",
                        "title": "formats supported (xml | json | ttl | mime type)",
                        "description": "A list of the formats supported by this implementation using their content types.",
                        "element_required": True,
                        "enum_values": ["formats", "json", "ttl", "mime"],
                        "element_property": True,
                    },
                    "_format": {
                        "items": {"type": "FHIRPrimitiveExtension"},
                        "type": "array",
                        "title": "Extension field for ``format``.",
                    },
                    "identifier": {
                        "items": {"type": "Identifier"},
                        "type": "array",
                        "title": "Additional identifier for the CapabilityStatement (business identifier)",
                        "description": "A formal identifier that is used to identify this CapabilityStatement when it is represented in other formats, or referenced in a specification, model, design or an instance.",
                        "element_property": True,
                    },
                    "implementation": {
                        "type": "CapabilityStatementImplementation",
                        "title": "If this describes a specific instance",
                        "description": "Identifies a specific implementation instance that is described by the capability statement - i.e. a particular installation, rather than the capabilities of a software program.",
                        "element_property": True,
                    },
                    "implementationGuide": {
                        "items": {"type": "string", "pattern": "\\S*"},
                        "type": "array",
                        "title": "Implementation guides supported",
                        "description": "A list of implementation guides that the server does (or should) support in their entirety.",
                        "enum_reference_types": ["ImplementationGuide"],
                        "element_property": True,
                    },
                    "_implementationGuide": {
                        "items": {"type": "FHIRPrimitiveExtension"},
                        "type": "array",
                        "title": "Extension field for ``implementationGuide``.",
                    },
                    "imports": {
                        "items": {"type": "string", "pattern": "\\S*"},
                        "type": "array",
                        "title": "Canonical URL of another capability statement this adds to",
                        "description": "Reference to a canonical URL of another CapabilityStatement that this software adds to. The capability statement automatically includes everything in the other statement, and it is not duplicated, though the server may repeat the same resources, interactions and operations to add additional details to them.",
                        "enum_reference_types": ["CapabilityStatement"],
                        "element_property": True,
                    },
                    "_imports": {
                        "items": {"type": "FHIRPrimitiveExtension"},
                        "type": "array",
                        "title": "Extension field for ``imports``.",
                    },
                    "instantiates": {
                        "items": {"type": "string", "pattern": "\\S*"},
                        "type": "array",
                        "title": "Canonical URL of another capability statement this implements",
                        "description": "Reference to a canonical URL of another CapabilityStatement that this software implements. This capability statement is a published API description that corresponds to a business service. The server may actually implement a subset of the capability statement it claims to implement, so the capability statement must specify the full capability details.",
                        "enum_reference_types": ["CapabilityStatement"],
                        "element_property": True,
                    },
                    "_instantiates": {
                        "items": {"type": "FHIRPrimitiveExtension"},
                        "type": "array",
                        "title": "Extension field for ``instantiates``.",
                    },
                    "jurisdiction": {
                        "items": {"type": "CodeableConcept"},
                        "type": "array",
                        "title": "Intended jurisdiction for capability statement (if applicable)",
                        "description": "A legal or geographic region in which the capability statement is intended to be used.",
                        "element_property": True,
                    },
                    "kind": {
                        "type": "string",
                        "pattern": "^[^\\s]+(\\s[^\\s]+)*$",
                        "title": "instance | capability | requirements",
                        "description": "The way that this statement is intended to be used, to describe an actual running instance of software, a particular product (kind, not instance of software) or a class of implementation (e.g. a desired purchase).",
                        "element_required": True,
                        "enum_values": ["instance", "capability", "requirements"],
                        "element_property": True,
                    },
                    "_kind": {
                        "type": "FHIRPrimitiveExtension",
                        "title": "Extension field for ``kind``.",
                    },
                    "messaging": {
                        "items": {"type": "CapabilityStatementMessaging"},
                        "type": "array",
                        "title": "If messaging is supported",
                        "description": "A description of the messaging capabilities of the solution.",
                        "element_property": True,
                    },
                    "name": {
                        "type": "string",
                        "pattern": "[ \\r\\n\\t\\S]+",
                        "title": "Name for this capability statement (computer friendly)",
                        "description": "A natural language name identifying the capability statement. This name should be usable as an identifier for the module by machine processing applications such as code generation.",
                        "element_property": True,
                    },
                    "_name": {
                        "type": "FHIRPrimitiveExtension",
                        "title": "Extension field for ``name``.",
                    },
                    "patchFormat": {
                        "items": {
                            "type": "string",
                            "pattern": "^[^\\s]+(\\s[^\\s]+)*$",
                        },
                        "type": "array",
                        "title": "Patch formats supported",
                        "description": "A list of the patch formats supported by this implementation using their content types.",
                        "element_property": True,
                    },
                    "_patchFormat": {
                        "items": {"type": "FHIRPrimitiveExtension"},
                        "type": "array",
                        "title": "Extension field for ``patchFormat``.",
                    },
                    "publisher": {
                        "type": "string",
                        "pattern": "[ \\r\\n\\t\\S]+",
                        "title": "Name of the publisher/steward (organization or individual)",
                        "description": "The name of the organization or individual responsible for the release and ongoing maintenance of the capability statement.",
                        "element_property": True,
                    },
                    "_publisher": {
                        "type": "FHIRPrimitiveExtension",
                        "title": "Extension field for ``publisher``.",
                    },
                    "purpose": {
                        "type": "string",
                        "pattern": "\\s*(\\S|\\s)*",
                        "title": "Why this capability statement is defined",
                        "description": "Explanation of why this capability statement is needed and why it has been designed as it has.",
                        "element_property": True,
                    },
                    "_purpose": {
                        "type": "FHIRPrimitiveExtension",
                        "title": "Extension field for ``purpose``.",
                    },
                    "rest": {
                        "items": {"type": "CapabilityStatementRest"},
                        "type": "array",
                        "title": "If the endpoint is a RESTful one",
                        "description": "A definition of the restful capabilities of the solution, if any.",
                        "element_property": True,
                    },
                    "software": {
                        "type": "CapabilityStatementSoftware",
                        "title": "Software that is covered by this capability statement",
                        "description": "Software that is covered by this capability statement.  It is used when the capability statement describes the capabilities of a particular software version, independent of an installation.",
                        "element_property": True,
                    },
                    "status": {
                        "type": "string",
                        "pattern": "^[^\\s]+(\\s[^\\s]+)*$",
                        "title": "draft | active | retired | unknown",
                        "description": "The status of this capability statement. Enables tracking the life-cycle of the content.",
                        "element_required": True,
                        "enum_values": ["draft", "active", "retired", "unknown"],
                        "element_property": True,
                    },
                    "_status": {
                        "type": "FHIRPrimitiveExtension",
                        "title": "Extension field for ``status``.",
                    },
                    "title": {
                        "type": "string",
                        "pattern": "[ \\r\\n\\t\\S]+",
                        "title": "Name for this capability statement (human friendly)",
                        "description": "A short, descriptive, user-friendly title for the capability statement.",
                        "element_property": True,
                    },
                    "_title": {
                        "type": "FHIRPrimitiveExtension",
                        "title": "Extension field for ``title``.",
                    },
                    "url": {
                        "type": "string",
                        "pattern": "\\S*",
                        "title": "Canonical identifier for this capability statement, represented as a URI (globally unique)",
                        "description": "An absolute URI that is used to identify this capability statement when it is referenced in a specification, model, design or an instance; also called its canonical identifier. This SHOULD be globally unique and SHOULD be a literal address at which an authoritative instance of this capability statement is (or will be) published. This URL can be the target of a canonical reference. It SHALL remain the same when the capability statement is stored on different servers.",
                        "element_property": True,
                    },
                    "_url": {
                        "type": "FHIRPrimitiveExtension",
                        "title": "Extension field for ``url``.",
                    },
                    "useContext": {
                        "items": {"type": "UsageContext"},
                        "type": "array",
                        "title": "The context that the content is intended to support",
                        "description": "The content was developed with a focus and intent of supporting the contexts that are listed. These contexts may be general categories (gender, age, ...) or may be references to specific programs (insurance plans, studies, ...) and may be used to assist with indexing and searching for appropriate capability statement instances.",
                        "element_property": True,
                    },
                    "version": {
                        "type": "string",
                        "pattern": "[ \\r\\n\\t\\S]+",
                        "title": "Business version of the capability statement",
                        "description": "The identifier that is used to identify this version of the capability statement when it is referenced in a specification, model, design or instance. This is an arbitrary value managed by the capability statement author and is not expected to be globally unique. For example, it might be a timestamp (e.g. yyyymmdd) if a managed version is not available. There is also no expectation that versions can be placed in a lexicographical sequence.",
                        "element_property": True,
                    },
                    "_version": {
                        "type": "FHIRPrimitiveExtension",
                        "title": "Extension field for ``version``.",
                    },
                    "versionAlgorithmCoding": {
                        "type": "Coding",
                        "title": "How to compare versions",
                        "description": "Indicates the mechanism used to compare versions to determine which is more current.",
                        "one_of_many_required": False,
                        "element_property": True,
                        "one_of_many": "versionAlgorithm",
                    },
                    "versionAlgorithmString": {
                        "type": "string",
                        "pattern": "[ \\r\\n\\t\\S]+",
                        "title": "How to compare versions",
                        "description": "Indicates the mechanism used to compare versions to determine which is more current.",
                        "one_of_many_required": False,
                        "element_property": True,
                        "one_of_many": "versionAlgorithm",
                    },
                    "_versionAlgorithmString": {
                        "type": "FHIRPrimitiveExtension",
                        "title": "Extension field for ``versionAlgorithmString``.",
                    },
                },
                "additionalProperties": False,
                "type": "object",
                "title": "CapabilityStatement",
                "description": "Disclaimer: Any field name ends with ``__ext`` doesn't part of\nResource StructureDefinition, instead used to enable Extensibility feature\nfor FHIR Primitive Data Types.\n\nA statement of system capabilities.\nA Capability Statement documents a set of capabilities (behaviors) of a\nFHIR Server or Client for a particular version of FHIR that may be used as\na statement of actual server functionality or a statement of required or\ndesired server implementation.",
            },
            "HTTPValidationError": {
                "properties": {
                    "detail": {
                        "items": {"$ref": "#/components/schemas/ValidationError"},
                        "type": "array",
                        "title": "Detail",
                    }
                },
                "type": "object",
                "title": "HTTPValidationError",
            },
            "OperationOutcome": {
                "properties": {
                    "resource_type": {
                        "type": "string",
                        "const": "OperationOutcome",
                        "title": "Resource Type",
                        "default": "OperationOutcome",
                    },
                    "fhir_comments": {
                        "anyOf": [
                            {"type": "string"},
                            {"items": {"type": "string"}, "type": "array"},
                        ],
                        "title": "Fhir Comments",
                        "element_property": False,
                    },
                    "id": {
                        "type": "string",
                        "maxLength": 64,
                        "minLength": 1,
                        "pattern": "^[A-Za-z0-9\\-.]+$",
                        "title": "Logical id of this artifact",
                        "description": "The logical id of the resource, as used in the URL for the resource. Once assigned, this value never changes.",
                        "element_property": True,
                    },
                    "implicitRules": {
                        "type": "string",
                        "pattern": "\\S*",
                        "title": "A set of rules under which this content was created",
                        "description": "A reference to a set of rules that were followed when the resource was constructed, and which must be understood when processing the content. Often, this is a reference to an implementation guide that defines the special rules along with other profiles etc.",
                        "element_property": True,
                    },
                    "_implicitRules": {
                        "type": "FHIRPrimitiveExtension",
                        "title": "Extension field for ``implicitRules``.",
                    },
                    "language": {
                        "type": "string",
                        "pattern": "^[^\\s]+(\\s[^\\s]+)*$",
                        "title": "Language of the resource content",
                        "description": "The base language in which the resource is written.",
                        "element_property": True,
                    },
                    "_language": {
                        "type": "FHIRPrimitiveExtension",
                        "title": "Extension field for ``language``.",
                    },
                    "meta": {
                        "type": "Meta",
                        "title": "Metadata about the resource",
                        "description": "The metadata about the resource. This is content that is maintained by the infrastructure. Changes to the content might not always be associated with version changes to the resource.",
                        "element_property": True,
                    },
                    "contained": {
                        "items": {"type": "Resource"},
                        "type": "array",
                        "title": "Contained, inline Resources",
                        "description": "These resources do not have an independent existence apart from the resource that contains them - they cannot be identified independently, nor can they have their own independent transaction scope. This is allowed to be a Parameters resource if and only if it is referenced by a resource that provides context/meaning.",
                        "element_property": True,
                    },
                    "extension": {
                        "items": {"type": "Extension"},
                        "type": "array",
                        "title": "Additional content defined by implementations",
                        "description": "May be used to represent additional information that is not part of the basic definition of the resource. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
                        "element_property": True,
                    },
                    "modifierExtension": {
                        "items": {"type": "Extension"},
                        "type": "array",
                        "title": "Extensions that cannot be ignored",
                        "description": "May be used to represent additional information that is not part of the basic definition of the resource and that modifies the understanding of the element that contains it and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer is allowed to define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions.  Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
                        "element_property": True,
                    },
                    "text": {
                        "type": "Narrative",
                        "title": "Text summary of the resource, for human interpretation",
                        "description": 'A human-readable narrative that contains a summary of the resource and can be used to represent the content of the resource to a human. The narrative need not encode all the structured data, but is required to contain sufficient detail to make it "clinically safe" for a human to just read the narrative. Resource definitions may define what content should be represented in the narrative to ensure clinical safety.',
                        "element_property": True,
                    },
                    "issue": {
                        "items": {"type": "OperationOutcomeIssue"},
                        "type": "array",
                        "title": "A single issue associated with the action",
                        "description": "An error, warning, or information message that results from a system action.",
                        "element_property": True,
                    },
                },
                "additionalProperties": False,
                "type": "object",
                "required": ["issue"],
                "title": "OperationOutcome",
                "description": "Disclaimer: Any field name ends with ``__ext`` doesn't part of\nResource StructureDefinition, instead used to enable Extensibility feature\nfor FHIR Primitive Data Types.\n\nInformation about the success/failure of an action.\nA collection of error, warning, or information messages that result from a\nsystem action.",
            },
            "Patient": {
                "properties": {
                    "resource_type": {
                        "type": "string",
                        "const": "Patient",
                        "title": "Resource Type",
                        "default": "Patient",
                    },
                    "fhir_comments": {
                        "anyOf": [
                            {"type": "string"},
                            {"items": {"type": "string"}, "type": "array"},
                        ],
                        "title": "Fhir Comments",
                        "element_property": False,
                    },
                    "id": {
                        "type": "string",
                        "maxLength": 64,
                        "minLength": 1,
                        "pattern": "^[A-Za-z0-9\\-.]+$",
                        "title": "Logical id of this artifact",
                        "description": "The logical id of the resource, as used in the URL for the resource. Once assigned, this value never changes.",
                        "element_property": True,
                    },
                    "implicitRules": {
                        "type": "string",
                        "pattern": "\\S*",
                        "title": "A set of rules under which this content was created",
                        "description": "A reference to a set of rules that were followed when the resource was constructed, and which must be understood when processing the content. Often, this is a reference to an implementation guide that defines the special rules along with other profiles etc.",
                        "element_property": True,
                    },
                    "_implicitRules": {
                        "type": "FHIRPrimitiveExtension",
                        "title": "Extension field for ``implicitRules``.",
                    },
                    "language": {
                        "type": "string",
                        "pattern": "^[^\\s]+(\\s[^\\s]+)*$",
                        "title": "Language of the resource content",
                        "description": "The base language in which the resource is written.",
                        "element_property": True,
                    },
                    "_language": {
                        "type": "FHIRPrimitiveExtension",
                        "title": "Extension field for ``language``.",
                    },
                    "meta": {
                        "type": "Meta",
                        "title": "Metadata about the resource",
                        "description": "The metadata about the resource. This is content that is maintained by the infrastructure. Changes to the content might not always be associated with version changes to the resource.",
                        "element_property": True,
                    },
                    "contained": {
                        "items": {"type": "Resource"},
                        "type": "array",
                        "title": "Contained, inline Resources",
                        "description": "These resources do not have an independent existence apart from the resource that contains them - they cannot be identified independently, nor can they have their own independent transaction scope. This is allowed to be a Parameters resource if and only if it is referenced by a resource that provides context/meaning.",
                        "element_property": True,
                    },
                    "extension": {
                        "items": {"type": "Extension"},
                        "type": "array",
                        "title": "Additional content defined by implementations",
                        "description": "May be used to represent additional information that is not part of the basic definition of the resource. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
                        "element_property": True,
                    },
                    "modifierExtension": {
                        "items": {"type": "Extension"},
                        "type": "array",
                        "title": "Extensions that cannot be ignored",
                        "description": "May be used to represent additional information that is not part of the basic definition of the resource and that modifies the understanding of the element that contains it and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer is allowed to define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions.  Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
                        "element_property": True,
                    },
                    "text": {
                        "type": "Narrative",
                        "title": "Text summary of the resource, for human interpretation",
                        "description": 'A human-readable narrative that contains a summary of the resource and can be used to represent the content of the resource to a human. The narrative need not encode all the structured data, but is required to contain sufficient detail to make it "clinically safe" for a human to just read the narrative. Resource definitions may define what content should be represented in the narrative to ensure clinical safety.',
                        "element_property": True,
                    },
                    "active": {
                        "type": "boolean",
                        "title": "Whether this patient's record is in active use",
                        "description": "Whether this patient record is in active use.  Many systems use this property to mark as non-current patients, such as those that have not been seen for a period of time based on an organization's business rules.  It is often used to filter patient lists to exclude inactive patients  Deceased patients may also be marked as inactive for the same reasons, but may be active for some time after death.",
                        "element_property": True,
                    },
                    "_active": {
                        "type": "FHIRPrimitiveExtension",
                        "title": "Extension field for ``active``.",
                    },
                    "address": {
                        "items": {"type": "Address"},
                        "type": "array",
                        "title": "An address for the individual",
                        "element_property": True,
                    },
                    "birthDate": {
                        "type": "string",
                        "format": "date",
                        "title": "The date of birth for the individual",
                        "element_property": True,
                    },
                    "_birthDate": {
                        "type": "FHIRPrimitiveExtension",
                        "title": "Extension field for ``birthDate``.",
                    },
                    "communication": {
                        "items": {"type": "PatientCommunication"},
                        "type": "array",
                        "title": "A language which may be used to communicate with the patient about his or her health",
                        "element_property": True,
                    },
                    "contact": {
                        "items": {"type": "PatientContact"},
                        "type": "array",
                        "title": "A contact party (e.g. guardian, partner, friend) for the patient",
                        "element_property": True,
                    },
                    "deceasedBoolean": {
                        "type": "boolean",
                        "title": "Indicates if the individual is deceased or not",
                        "one_of_many_required": False,
                        "element_property": True,
                        "one_of_many": "deceased",
                    },
                    "_deceasedBoolean": {
                        "type": "FHIRPrimitiveExtension",
                        "title": "Extension field for ``deceasedBoolean``.",
                    },
                    "deceasedDateTime": {
                        "type": "string",
                        "format": "date-time",
                        "title": "Indicates if the individual is deceased or not",
                        "one_of_many_required": False,
                        "element_property": True,
                        "one_of_many": "deceased",
                    },
                    "_deceasedDateTime": {
                        "type": "FHIRPrimitiveExtension",
                        "title": "Extension field for ``deceasedDateTime``.",
                    },
                    "gender": {
                        "type": "string",
                        "pattern": "^[^\\s]+(\\s[^\\s]+)*$",
                        "title": "male | female | other | unknown",
                        "description": "Administrative Gender - the gender that the patient is considered to have for administration and record keeping purposes.",
                        "enum_values": ["male", "female", "other", "unknown"],
                        "element_property": True,
                    },
                    "_gender": {
                        "type": "FHIRPrimitiveExtension",
                        "title": "Extension field for ``gender``.",
                    },
                    "generalPractitioner": {
                        "items": {"type": "Reference"},
                        "type": "array",
                        "title": "Patient's nominated primary care provider",
                        "description": "Patient's nominated care provider.",
                        "enum_reference_types": [
                            "Organization",
                            "Practitioner",
                            "PractitionerRole",
                        ],
                        "element_property": True,
                    },
                    "identifier": {
                        "items": {"type": "Identifier"},
                        "type": "array",
                        "title": "An identifier for this patient",
                        "element_property": True,
                    },
                    "link": {
                        "items": {"type": "PatientLink"},
                        "type": "array",
                        "title": "Link to a Patient or RelatedPerson resource that concerns the same actual individual",
                        "element_property": True,
                    },
                    "managingOrganization": {
                        "type": "Reference",
                        "title": "Organization that is the custodian of the patient record",
                        "enum_reference_types": ["Organization"],
                        "element_property": True,
                    },
                    "maritalStatus": {
                        "type": "CodeableConcept",
                        "title": "Marital (civil) status of a patient",
                        "description": "This field contains a patient's most recent marital (civil) status.",
                        "element_property": True,
                    },
                    "multipleBirthBoolean": {
                        "type": "boolean",
                        "title": "Whether patient is part of a multiple birth",
                        "description": "Indicates whether the patient is part of a multiple (boolean) or indicates the actual birth order (integer).",
                        "one_of_many_required": False,
                        "element_property": True,
                        "one_of_many": "multipleBirth",
                    },
                    "_multipleBirthBoolean": {
                        "type": "FHIRPrimitiveExtension",
                        "title": "Extension field for ``multipleBirthBoolean``.",
                    },
                    "multipleBirthInteger": {
                        "type": "integer",
                        "title": "Whether patient is part of a multiple birth",
                        "description": "Indicates whether the patient is part of a multiple (boolean) or indicates the actual birth order (integer).",
                        "one_of_many_required": False,
                        "element_property": True,
                        "one_of_many": "multipleBirth",
                    },
                    "_multipleBirthInteger": {
                        "type": "FHIRPrimitiveExtension",
                        "title": "Extension field for ``multipleBirthInteger``.",
                    },
                    "name": {
                        "items": {"type": "HumanName"},
                        "type": "array",
                        "title": "A name associated with the patient",
                        "description": "A name associated with the individual.",
                        "element_property": True,
                    },
                    "photo": {
                        "items": {"type": "Attachment"},
                        "type": "array",
                        "title": "Image of the patient",
                        "element_property": True,
                    },
                    "telecom": {
                        "items": {"type": "ContactPoint"},
                        "type": "array",
                        "title": "A contact detail for the individual",
                        "description": "A contact detail (e.g. a telephone number or an email address) by which the individual may be contacted.",
                        "element_property": True,
                    },
                },
                "additionalProperties": False,
                "type": "object",
                "title": "Patient",
                "description": "Disclaimer: Any field name ends with ``__ext`` doesn't part of\nResource StructureDefinition, instead used to enable Extensibility feature\nfor FHIR Primitive Data Types.\n\nInformation about an individual or animal receiving health care services.\nDemographics and other administrative information about an individual or\nanimal receiving care or other health-related services.",
            },
            "Practitioner": {
                "properties": {
                    "resource_type": {
                        "type": "string",
                        "const": "Practitioner",
                        "title": "Resource Type",
                        "default": "Practitioner",
                    },
                    "fhir_comments": {
                        "anyOf": [
                            {"type": "string"},
                            {"items": {"type": "string"}, "type": "array"},
                        ],
                        "title": "Fhir Comments",
                        "element_property": False,
                    },
                    "id": {
                        "type": "string",
                        "maxLength": 64,
                        "minLength": 1,
                        "pattern": "^[A-Za-z0-9\\-.]+$",
                        "title": "Logical id of this artifact",
                        "description": "The logical id of the resource, as used in the URL for the resource. Once assigned, this value never changes.",
                        "element_property": True,
                    },
                    "implicitRules": {
                        "type": "string",
                        "pattern": "\\S*",
                        "title": "A set of rules under which this content was created",
                        "description": "A reference to a set of rules that were followed when the resource was constructed, and which must be understood when processing the content. Often, this is a reference to an implementation guide that defines the special rules along with other profiles etc.",
                        "element_property": True,
                    },
                    "_implicitRules": {
                        "type": "FHIRPrimitiveExtension",
                        "title": "Extension field for ``implicitRules``.",
                    },
                    "language": {
                        "type": "string",
                        "pattern": "^[^\\s]+(\\s[^\\s]+)*$",
                        "title": "Language of the resource content",
                        "description": "The base language in which the resource is written.",
                        "element_property": True,
                    },
                    "_language": {
                        "type": "FHIRPrimitiveExtension",
                        "title": "Extension field for ``language``.",
                    },
                    "meta": {
                        "type": "Meta",
                        "title": "Metadata about the resource",
                        "description": "The metadata about the resource. This is content that is maintained by the infrastructure. Changes to the content might not always be associated with version changes to the resource.",
                        "element_property": True,
                    },
                    "contained": {
                        "items": {"type": "Resource"},
                        "type": "array",
                        "title": "Contained, inline Resources",
                        "description": "These resources do not have an independent existence apart from the resource that contains them - they cannot be identified independently, nor can they have their own independent transaction scope. This is allowed to be a Parameters resource if and only if it is referenced by a resource that provides context/meaning.",
                        "element_property": True,
                    },
                    "extension": {
                        "items": {"type": "Extension"},
                        "type": "array",
                        "title": "Additional content defined by implementations",
                        "description": "May be used to represent additional information that is not part of the basic definition of the resource. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
                        "element_property": True,
                    },
                    "modifierExtension": {
                        "items": {"type": "Extension"},
                        "type": "array",
                        "title": "Extensions that cannot be ignored",
                        "description": "May be used to represent additional information that is not part of the basic definition of the resource and that modifies the understanding of the element that contains it and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer is allowed to define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions.  Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
                        "element_property": True,
                    },
                    "text": {
                        "type": "Narrative",
                        "title": "Text summary of the resource, for human interpretation",
                        "description": 'A human-readable narrative that contains a summary of the resource and can be used to represent the content of the resource to a human. The narrative need not encode all the structured data, but is required to contain sufficient detail to make it "clinically safe" for a human to just read the narrative. Resource definitions may define what content should be represented in the narrative to ensure clinical safety.',
                        "element_property": True,
                    },
                    "active": {
                        "type": "boolean",
                        "title": "Whether this practitioner's record is in active use",
                        "element_property": True,
                    },
                    "_active": {
                        "type": "FHIRPrimitiveExtension",
                        "title": "Extension field for ``active``.",
                    },
                    "address": {
                        "items": {"type": "Address"},
                        "type": "array",
                        "title": "Address(es) of the practitioner that are not role specific (typically home address)",
                        "description": "Address(es) of the practitioner that are not role specific (typically home address).  Work addresses are not typically entered in this property as they are usually role dependent.",
                        "element_property": True,
                    },
                    "birthDate": {
                        "type": "string",
                        "format": "date",
                        "title": "The date  on which the practitioner was born",
                        "description": "The date of birth for the practitioner.",
                        "element_property": True,
                    },
                    "_birthDate": {
                        "type": "FHIRPrimitiveExtension",
                        "title": "Extension field for ``birthDate``.",
                    },
                    "communication": {
                        "items": {"type": "PractitionerCommunication"},
                        "type": "array",
                        "title": "A language which may be used to communicate with the practitioner",
                        "description": "A language which may be used to communicate with the practitioner, often for correspondence/administrative purposes.  The `PractitionerRole.communication` property should be used for publishing the languages that a practitioner is able to communicate with patients (on a per Organization/Role basis).",
                        "element_property": True,
                    },
                    "deceasedBoolean": {
                        "type": "boolean",
                        "title": "Indicates if the practitioner is deceased or not",
                        "one_of_many_required": False,
                        "element_property": True,
                        "one_of_many": "deceased",
                    },
                    "_deceasedBoolean": {
                        "type": "FHIRPrimitiveExtension",
                        "title": "Extension field for ``deceasedBoolean``.",
                    },
                    "deceasedDateTime": {
                        "type": "string",
                        "format": "date-time",
                        "title": "Indicates if the practitioner is deceased or not",
                        "one_of_many_required": False,
                        "element_property": True,
                        "one_of_many": "deceased",
                    },
                    "_deceasedDateTime": {
                        "type": "FHIRPrimitiveExtension",
                        "title": "Extension field for ``deceasedDateTime``.",
                    },
                    "gender": {
                        "type": "string",
                        "pattern": "^[^\\s]+(\\s[^\\s]+)*$",
                        "title": "male | female | other | unknown",
                        "description": "Administrative Gender - the gender that the person is considered to have for administration and record keeping purposes.",
                        "enum_values": ["male", "female", "other", "unknown"],
                        "element_property": True,
                    },
                    "_gender": {
                        "type": "FHIRPrimitiveExtension",
                        "title": "Extension field for ``gender``.",
                    },
                    "identifier": {
                        "items": {"type": "Identifier"},
                        "type": "array",
                        "title": "An identifier for the person as this agent",
                        "description": "An identifier that applies to this person in this role.",
                        "element_property": True,
                    },
                    "name": {
                        "items": {"type": "HumanName"},
                        "type": "array",
                        "title": "The name(s) associated with the practitioner",
                        "element_property": True,
                    },
                    "photo": {
                        "items": {"type": "Attachment"},
                        "type": "array",
                        "title": "Image of the person",
                        "element_property": True,
                    },
                    "qualification": {
                        "items": {"type": "PractitionerQualification"},
                        "type": "array",
                        "title": "Qualifications, certifications, accreditations, licenses, training, etc. pertaining to the provision of care",
                        "description": "The official qualifications, certifications, accreditations, training, licenses (and other types of educations/skills/capabilities) that authorize or otherwise pertain to the provision of care by the practitioner.  For example, a medical license issued by a medical board of licensure authorizing the practitioner to practice medicine within a certain locality.",
                        "element_property": True,
                    },
                    "telecom": {
                        "items": {"type": "ContactPoint"},
                        "type": "array",
                        "title": "A contact detail for the practitioner (that apply to all roles)",
                        "description": "A contact detail for the practitioner, e.g. a telephone number or an email address.",
                        "element_property": True,
                    },
                },
                "additionalProperties": False,
                "type": "object",
                "title": "Practitioner",
                "description": "Disclaimer: Any field name ends with ``__ext`` doesn't part of\nResource StructureDefinition, instead used to enable Extensibility feature\nfor FHIR Primitive Data Types.\n\nA person with a  formal responsibility in the provisioning of healthcare or\nrelated services.\nA person who is directly or indirectly involved in the provisioning of\nhealthcare or related services.",
            },
            "PractitionerCustom": {
                "title": "PractitionerCustom",
                "description": "Disclaimer: Any field name ends with ``__ext`` doesn't part of\nResource StructureDefinition, instead used to enable Extensibility feature\nfor FHIR Primitive Data Types.\n\nA person with a  formal responsibility in the provisioning of healthcare or\nrelated services.\nA person who is directly or indirectly involved in the provisioning of\nhealthcare or related services.",
                "type": "object",
                "properties": {
                    "resource_type": {
                        "title": "Resource Type",
                        "default": "Practitioner",
                        "const": "Practitioner",
                        "type": "string",
                    },
                    "fhir_comments": {
                        "title": "Fhir Comments",
                        "element_property": False,
                        "anyOf": [
                            {"type": "string"},
                            {"type": "array", "items": {"type": "string"}},
                        ],
                    },
                    "id": {
                        "title": "Logical id of this artifact",
                        "description": "The logical id of the resource, as used in the URL for the resource. Once assigned, this value never changes.",
                        "element_property": True,
                        "minLength": 1,
                        "maxLength": 64,
                        "pattern": "^[A-Za-z0-9\\-.]+$",
                        "type": "string",
                    },
                    "implicitRules": {
                        "title": "A set of rules under which this content was created",
                        "description": "A reference to a set of rules that were followed when the resource was constructed, and which must be understood when processing the content. Often, this is a reference to an implementation guide that defines the special rules along with other profiles etc.",
                        "element_property": True,
                        "pattern": "\\S*",
                        "type": "string",
                    },
                    "_implicitRules": {
                        "title": "Extension field for ``implicitRules``.",
                        "type": "FHIRPrimitiveExtension",
                    },
                    "language": {
                        "title": "Language of the resource content",
                        "description": "The base language in which the resource is written.",
                        "element_property": True,
                        "pattern": "^[^\\s]+(\\s[^\\s]+)*$",
                        "type": "string",
                    },
                    "_language": {
                        "title": "Extension field for ``language``.",
                        "type": "FHIRPrimitiveExtension",
                    },
                    "meta": {
                        "title": "Metadata about the resource",
                        "description": "The metadata about the resource. This is content that is maintained by the infrastructure. Changes to the content might not always be associated with version changes to the resource.",
                        "element_property": True,
                        "type": "Meta",
                    },
                    "contained": {
                        "title": "Contained, inline Resources",
                        "description": "These resources do not have an independent existence apart from the resource that contains them - they cannot be identified independently, nor can they have their own independent transaction scope. This is allowed to be a Parameters resource if and only if it is referenced by a resource that provides context/meaning.",
                        "element_property": True,
                        "type": "array",
                        "items": {"type": "Resource"},
                    },
                    "extension": {
                        "title": "Additional content defined by implementations",
                        "description": "May be used to represent additional information that is not part of the basic definition of the resource. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer can define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension.",
                        "element_property": True,
                        "type": "array",
                        "items": {"type": "Extension"},
                    },
                    "modifierExtension": {
                        "title": "Extensions that cannot be ignored",
                        "description": "May be used to represent additional information that is not part of the basic definition of the resource and that modifies the understanding of the element that contains it and/or the understanding of the containing element's descendants. Usually modifier elements provide negation or qualification. To make the use of extensions safe and managable, there is a strict set of governance applied to the definition and use of extensions. Though any implementer is allowed to define an extension, there is a set of requirements that SHALL be met as part of the definition of the extension. Applications processing a resource are required to check for modifier extensions.  Modifier extensions SHALL NOT change the meaning of any elements on Resource or DomainResource (including cannot change the meaning of modifierExtension itself).",
                        "element_property": True,
                        "type": "array",
                        "items": {"type": "Extension"},
                    },
                    "text": {
                        "title": "Text summary of the resource, for human interpretation",
                        "description": 'A human-readable narrative that contains a summary of the resource and can be used to represent the content of the resource to a human. The narrative need not encode all the structured data, but is required to contain sufficient detail to make it "clinically safe" for a human to just read the narrative. Resource definitions may define what content should be represented in the narrative to ensure clinical safety.',
                        "element_property": True,
                        "type": "Narrative",
                    },
                    "active": {
                        "title": "Whether this practitioner's record is in active use",
                        "element_property": True,
                        "type": "boolean",
                    },
                    "_active": {
                        "title": "Extension field for ``active``.",
                        "type": "FHIRPrimitiveExtension",
                    },
                    "address": {
                        "title": "Address(es) of the practitioner that are not role specific (typically home address)",
                        "description": "Address(es) of the practitioner that are not role specific (typically home address).  Work addresses are not typically entered in this property as they are usually role dependent.",
                        "element_property": True,
                        "type": "array",
                        "items": {"type": "Address"},
                    },
                    "birthDate": {
                        "title": "The date  on which the practitioner was born",
                        "description": "The date of birth for the practitioner.",
                        "element_property": True,
                        "type": "string",
                        "format": "date",
                    },
                    "_birthDate": {
                        "title": "Extension field for ``birthDate``.",
                        "type": "FHIRPrimitiveExtension",
                    },
                    "communication": {
                        "title": "A language which may be used to communicate with the practitioner",
                        "description": "A language which may be used to communicate with the practitioner, often for correspondence/administrative purposes.  The `PractitionerRole.communication` property should be used for publishing the languages that a practitioner is able to communicate with patients (on a per Organization/Role basis).",
                        "element_property": True,
                        "type": "array",
                        "items": {"type": "PractitionerCommunication"},
                    },
                    "deceasedBoolean": {
                        "title": "Indicates if the practitioner is deceased or not",
                        "element_property": True,
                        "one_of_many": "deceased",
                        "one_of_many_required": False,
                        "type": "boolean",
                    },
                    "_deceasedBoolean": {
                        "title": "Extension field for ``deceasedBoolean``.",
                        "type": "FHIRPrimitiveExtension",
                    },
                    "deceasedDateTime": {
                        "title": "Indicates if the practitioner is deceased or not",
                        "element_property": True,
                        "one_of_many": "deceased",
                        "one_of_many_required": False,
                        "type": "string",
                        "format": "date-time",
                    },
                    "_deceasedDateTime": {
                        "title": "Extension field for ``deceasedDateTime``.",
                        "type": "FHIRPrimitiveExtension",
                    },
                    "gender": {
                        "title": "male | female | other | unknown",
                        "description": "Administrative Gender - the gender that the person is considered to have for administration and record keeping purposes.",
                        "element_property": True,
                        "enum_values": ["male", "female", "other", "unknown"],
                        "pattern": "^[^\\s]+(\\s[^\\s]+)*$",
                        "type": "string",
                    },
                    "_gender": {
                        "title": "Extension field for ``gender``.",
                        "type": "FHIRPrimitiveExtension",
                    },
                    "identifier": {
                        "title": "An identifier for the person as this agent",
                        "description": "An identifier that applies to this person in this role.",
                        "element_property": True,
                        "type": "array",
                        "items": {"type": "Identifier"},
                    },
                    "name": {
                        "title": "The name(s) associated with the practitioner",
                        "element_property": True,
                        "type": "array",
                        "items": {"type": "HumanName"},
                    },
                    "photo": {
                        "title": "Image of the person",
                        "element_property": True,
                        "type": "array",
                        "items": {"type": "Attachment"},
                    },
                    "qualification": {
                        "title": "Qualifications, certifications, accreditations, licenses, training, etc. pertaining to the provision of care",
                        "description": "The official qualifications, certifications, accreditations, training, licenses (and other types of educations/skills/capabilities) that authorize or otherwise pertain to the provision of care by the practitioner.  For example, a medical license issued by a medical board of licensure authorizing the practitioner to practice medicine within a certain locality.",
                        "element_property": True,
                        "type": "array",
                        "items": {"type": "PractitionerQualification"},
                    },
                    "telecom": {
                        "title": "A contact detail for the practitioner (that apply to all roles)",
                        "description": "A contact detail for the practitioner, e.g. a telephone number or an email address.",
                        "element_property": True,
                        "type": "array",
                        "items": {"type": "ContactPoint"},
                    },
                },
                "additionalProperties": False,
                "example": {
                    "resourceType": "Practitioner",
                    "id": "example",
                    "name": [
                        {"family": "Careful", "given": ["Adam"], "prefix": ["Dr"]}
                    ],
                },
            },
            "ValidationError": {
                "properties": {
                    "loc": {
                        "items": {"anyOf": [{"type": "string"}, {"type": "integer"}]},
                        "type": "array",
                        "title": "Location",
                    },
                    "msg": {"type": "string", "title": "Message"},
                    "type": {"type": "string", "title": "Error Type"},
                },
                "type": "object",
                "required": ["loc", "msg", "type"],
                "title": "ValidationError",
            },
        }
    },
}
