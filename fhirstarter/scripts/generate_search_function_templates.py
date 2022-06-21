from fhirstarter.search_parameters import (
    fhir_sp_name_to_var_sp_name,
    load_search_parameters,
)


def main() -> None:
    all_search_parameters = load_search_parameters()

    for resource_type, search_parameters in sorted(all_search_parameters.items()):
        if resource_type in {"Bundle", "DomainResource", "Resource"}:
            continue

        search_parameter_names = [
            fhir_sp_name_to_var_sp_name(name)
            for name in sorted(search_parameters.keys())
        ]

        function_template = f"""async def {resource_type.lower()}_search(request: Request, response: Response, {", ".join([f"{sp}: str" for sp in search_parameter_names])}) -> Bundle:
    result = cast(FHIRInteractionResult[Bundle], await callable_({", ".join([f"{sp}={sp}" for sp in search_parameter_names])}, request=request))

    return finalize_searchset(result)"""

        print(f"{function_template}\n")


if __name__ == "__main__":
    main()
