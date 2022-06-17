from typing import Any, cast

from fastapi import Request, Response
from fhir.resources.fhirtypes import Id

from .provider import FHIRInteractionResult, FHIRResourceType

resource_type_str: str | None = None


def resource_id(result: FHIRInteractionResult[FHIRResourceType]) -> Id | None:
    if result.id_ is not None:
        return result.id_

    if result.resource is not None:
        return result.resource.id

    return None


async def callable_(*_: Any, **__: Any) -> Any:
    return None


async def create(
    request: Request, response: Response, resource: FHIRResourceType
) -> FHIRResourceType | None:
    result = cast(FHIRInteractionResult[FHIRResourceType], await callable_(resource))
    result.validate()

    id_ = resource_id(result)

    response.headers["Location"] = (
        f"{request.base_url}{resource_type_str}" f"/{id_}/_history/1"
    )

    return result.resource


async def read(request: Request, response: Response, id_: Id) -> FHIRResourceType:
    result = cast(FHIRInteractionResult[FHIRResourceType], await callable_(id_))
    result.validate()

    assert result.resource is not None, "FHIR read interaction must return a resource"

    return result.resource


async def update(
    request: Request, response: Response, id_: Id, resource: FHIRResourceType
) -> FHIRResourceType | None:
    result = cast(
        FHIRInteractionResult[FHIRResourceType], await callable_(id_, resource)
    )
    result.validate()

    return result.resource


async def account_search(
    request: Request,
    response: Response,
    identifier: str,
    name: str,
    owner: str,
    patient: str,
    period: str,
    status: str,
    subject: str,
    type_: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            identifier=identifier,
            name=name,
            owner=owner,
            patient=patient,
            period=period,
            status=status,
            subject=subject,
            type_=type_,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def activitydefinition_search(
    request: Request,
    response: Response,
    composed_of: str,
    context: str,
    context_quantity: str,
    context_type: str,
    context_type_quantity: str,
    context_type_value: str,
    date: str,
    depends_on: str,
    derived_from: str,
    description: str,
    effective: str,
    identifier: str,
    jurisdiction: str,
    name: str,
    predecessor: str,
    publisher: str,
    status: str,
    successor: str,
    title: str,
    topic: str,
    url: str,
    version: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            composed_of=composed_of,
            context=context,
            context_quantity=context_quantity,
            context_type=context_type,
            context_type_quantity=context_type_quantity,
            context_type_value=context_type_value,
            date=date,
            depends_on=depends_on,
            derived_from=derived_from,
            description=description,
            effective=effective,
            identifier=identifier,
            jurisdiction=jurisdiction,
            name=name,
            predecessor=predecessor,
            publisher=publisher,
            status=status,
            successor=successor,
            title=title,
            topic=topic,
            url=url,
            version=version,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def adverseevent_search(
    request: Request,
    response: Response,
    actuality: str,
    category: str,
    date: str,
    event: str,
    location: str,
    recorder: str,
    resultingcondition: str,
    seriousness: str,
    severity: str,
    study: str,
    subject: str,
    substance: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            actuality=actuality,
            category=category,
            date=date,
            event=event,
            location=location,
            recorder=recorder,
            resultingcondition=resultingcondition,
            seriousness=seriousness,
            severity=severity,
            study=study,
            subject=subject,
            substance=substance,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def allergyintolerance_search(
    request: Request,
    response: Response,
    asserter: str,
    category: str,
    clinical_status: str,
    code: str,
    criticality: str,
    date: str,
    identifier: str,
    last_date: str,
    manifestation: str,
    onset: str,
    patient: str,
    recorder: str,
    route: str,
    severity: str,
    type_: str,
    verification_status: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            asserter=asserter,
            category=category,
            clinical_status=clinical_status,
            code=code,
            criticality=criticality,
            date=date,
            identifier=identifier,
            last_date=last_date,
            manifestation=manifestation,
            onset=onset,
            patient=patient,
            recorder=recorder,
            route=route,
            severity=severity,
            type_=type_,
            verification_status=verification_status,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def appointment_search(
    request: Request,
    response: Response,
    actor: str,
    appointment_type: str,
    based_on: str,
    date: str,
    identifier: str,
    location: str,
    part_status: str,
    patient: str,
    practitioner: str,
    reason_code: str,
    reason_reference: str,
    service_category: str,
    service_type: str,
    slot: str,
    specialty: str,
    status: str,
    supporting_info: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            actor=actor,
            appointment_type=appointment_type,
            based_on=based_on,
            date=date,
            identifier=identifier,
            location=location,
            part_status=part_status,
            patient=patient,
            practitioner=practitioner,
            reason_code=reason_code,
            reason_reference=reason_reference,
            service_category=service_category,
            service_type=service_type,
            slot=slot,
            specialty=specialty,
            status=status,
            supporting_info=supporting_info,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def appointmentresponse_search(
    request: Request,
    response: Response,
    actor: str,
    appointment: str,
    identifier: str,
    location: str,
    part_status: str,
    patient: str,
    practitioner: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            actor=actor,
            appointment=appointment,
            identifier=identifier,
            location=location,
            part_status=part_status,
            patient=patient,
            practitioner=practitioner,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def auditevent_search(
    request: Request,
    response: Response,
    action: str,
    address: str,
    agent: str,
    agent_name: str,
    agent_role: str,
    altid: str,
    date: str,
    entity: str,
    entity_name: str,
    entity_role: str,
    entity_type: str,
    outcome: str,
    patient: str,
    policy: str,
    site: str,
    source: str,
    subtype: str,
    type_: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            action=action,
            address=address,
            agent=agent,
            agent_name=agent_name,
            agent_role=agent_role,
            altid=altid,
            date=date,
            entity=entity,
            entity_name=entity_name,
            entity_role=entity_role,
            entity_type=entity_type,
            outcome=outcome,
            patient=patient,
            policy=policy,
            site=site,
            source=source,
            subtype=subtype,
            type_=type_,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def basic_search(
    request: Request,
    response: Response,
    author: str,
    code: str,
    created: str,
    identifier: str,
    patient: str,
    subject: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            author=author,
            code=code,
            created=created,
            identifier=identifier,
            patient=patient,
            subject=subject,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def bodystructure_search(
    request: Request,
    response: Response,
    identifier: str,
    location: str,
    morphology: str,
    patient: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            identifier=identifier,
            location=location,
            morphology=morphology,
            patient=patient,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def capabilitystatement_search(
    request: Request,
    response: Response,
    context: str,
    context_quantity: str,
    context_type: str,
    context_type_quantity: str,
    context_type_value: str,
    date: str,
    description: str,
    fhirversion: str,
    format_: str,
    guide: str,
    jurisdiction: str,
    mode: str,
    name: str,
    publisher: str,
    resource: str,
    resource_profile: str,
    security_service: str,
    software: str,
    status: str,
    supported_profile: str,
    title: str,
    url: str,
    version: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            context=context,
            context_quantity=context_quantity,
            context_type=context_type,
            context_type_quantity=context_type_quantity,
            context_type_value=context_type_value,
            date=date,
            description=description,
            fhirversion=fhirversion,
            format_=format_,
            guide=guide,
            jurisdiction=jurisdiction,
            mode=mode,
            name=name,
            publisher=publisher,
            resource=resource,
            resource_profile=resource_profile,
            security_service=security_service,
            software=software,
            status=status,
            supported_profile=supported_profile,
            title=title,
            url=url,
            version=version,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def careplan_search(
    request: Request,
    response: Response,
    activity_code: str,
    activity_date: str,
    activity_reference: str,
    based_on: str,
    care_team: str,
    category: str,
    condition: str,
    date: str,
    encounter: str,
    goal: str,
    identifier: str,
    instantiates_canonical: str,
    instantiates_uri: str,
    intent: str,
    part_of: str,
    patient: str,
    performer: str,
    replaces: str,
    status: str,
    subject: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            activity_code=activity_code,
            activity_date=activity_date,
            activity_reference=activity_reference,
            based_on=based_on,
            care_team=care_team,
            category=category,
            condition=condition,
            date=date,
            encounter=encounter,
            goal=goal,
            identifier=identifier,
            instantiates_canonical=instantiates_canonical,
            instantiates_uri=instantiates_uri,
            intent=intent,
            part_of=part_of,
            patient=patient,
            performer=performer,
            replaces=replaces,
            status=status,
            subject=subject,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def careteam_search(
    request: Request,
    response: Response,
    category: str,
    date: str,
    encounter: str,
    identifier: str,
    participant: str,
    patient: str,
    status: str,
    subject: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            category=category,
            date=date,
            encounter=encounter,
            identifier=identifier,
            participant=participant,
            patient=patient,
            status=status,
            subject=subject,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def chargeitem_search(
    request: Request,
    response: Response,
    account: str,
    code: str,
    context: str,
    entered_date: str,
    enterer: str,
    factor_override: str,
    identifier: str,
    occurrence: str,
    patient: str,
    performer_actor: str,
    performer_function: str,
    performing_organization: str,
    price_override: str,
    quantity: str,
    requesting_organization: str,
    service: str,
    subject: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            account=account,
            code=code,
            context=context,
            entered_date=entered_date,
            enterer=enterer,
            factor_override=factor_override,
            identifier=identifier,
            occurrence=occurrence,
            patient=patient,
            performer_actor=performer_actor,
            performer_function=performer_function,
            performing_organization=performing_organization,
            price_override=price_override,
            quantity=quantity,
            requesting_organization=requesting_organization,
            service=service,
            subject=subject,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def chargeitemdefinition_search(
    request: Request,
    response: Response,
    context: str,
    context_quantity: str,
    context_type: str,
    context_type_quantity: str,
    context_type_value: str,
    date: str,
    description: str,
    effective: str,
    identifier: str,
    jurisdiction: str,
    publisher: str,
    status: str,
    title: str,
    url: str,
    version: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            context=context,
            context_quantity=context_quantity,
            context_type=context_type,
            context_type_quantity=context_type_quantity,
            context_type_value=context_type_value,
            date=date,
            description=description,
            effective=effective,
            identifier=identifier,
            jurisdiction=jurisdiction,
            publisher=publisher,
            status=status,
            title=title,
            url=url,
            version=version,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def claim_search(
    request: Request,
    response: Response,
    care_team: str,
    created: str,
    detail_udi: str,
    encounter: str,
    enterer: str,
    facility: str,
    identifier: str,
    insurer: str,
    item_udi: str,
    patient: str,
    payee: str,
    priority: str,
    procedure_udi: str,
    provider: str,
    status: str,
    subdetail_udi: str,
    use: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            care_team=care_team,
            created=created,
            detail_udi=detail_udi,
            encounter=encounter,
            enterer=enterer,
            facility=facility,
            identifier=identifier,
            insurer=insurer,
            item_udi=item_udi,
            patient=patient,
            payee=payee,
            priority=priority,
            procedure_udi=procedure_udi,
            provider=provider,
            status=status,
            subdetail_udi=subdetail_udi,
            use=use,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def claimresponse_search(
    request: Request,
    response: Response,
    created: str,
    disposition: str,
    identifier: str,
    insurer: str,
    outcome: str,
    patient: str,
    payment_date: str,
    request_: str,
    requestor: str,
    status: str,
    use: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            created=created,
            disposition=disposition,
            identifier=identifier,
            insurer=insurer,
            outcome=outcome,
            patient=patient,
            payment_date=payment_date,
            request_=request_,
            requestor=requestor,
            status=status,
            use=use,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def clinicalimpression_search(
    request: Request,
    response: Response,
    assessor: str,
    date: str,
    encounter: str,
    finding_code: str,
    finding_ref: str,
    identifier: str,
    investigation: str,
    patient: str,
    previous: str,
    problem: str,
    status: str,
    subject: str,
    supporting_info: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            assessor=assessor,
            date=date,
            encounter=encounter,
            finding_code=finding_code,
            finding_ref=finding_ref,
            identifier=identifier,
            investigation=investigation,
            patient=patient,
            previous=previous,
            problem=problem,
            status=status,
            subject=subject,
            supporting_info=supporting_info,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def codesystem_search(
    request: Request,
    response: Response,
    code: str,
    content_mode: str,
    context: str,
    context_quantity: str,
    context_type: str,
    context_type_quantity: str,
    context_type_value: str,
    date: str,
    description: str,
    identifier: str,
    jurisdiction: str,
    language: str,
    name: str,
    publisher: str,
    status: str,
    supplements: str,
    system: str,
    title: str,
    url: str,
    version: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            code=code,
            content_mode=content_mode,
            context=context,
            context_quantity=context_quantity,
            context_type=context_type,
            context_type_quantity=context_type_quantity,
            context_type_value=context_type_value,
            date=date,
            description=description,
            identifier=identifier,
            jurisdiction=jurisdiction,
            language=language,
            name=name,
            publisher=publisher,
            status=status,
            supplements=supplements,
            system=system,
            title=title,
            url=url,
            version=version,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def communication_search(
    request: Request,
    response: Response,
    based_on: str,
    category: str,
    encounter: str,
    identifier: str,
    instantiates_canonical: str,
    instantiates_uri: str,
    medium: str,
    part_of: str,
    patient: str,
    received: str,
    recipient: str,
    sender: str,
    sent: str,
    status: str,
    subject: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            based_on=based_on,
            category=category,
            encounter=encounter,
            identifier=identifier,
            instantiates_canonical=instantiates_canonical,
            instantiates_uri=instantiates_uri,
            medium=medium,
            part_of=part_of,
            patient=patient,
            received=received,
            recipient=recipient,
            sender=sender,
            sent=sent,
            status=status,
            subject=subject,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def communicationrequest_search(
    request: Request,
    response: Response,
    authored: str,
    based_on: str,
    category: str,
    encounter: str,
    group_identifier: str,
    identifier: str,
    medium: str,
    occurrence: str,
    patient: str,
    priority: str,
    recipient: str,
    replaces: str,
    requester: str,
    sender: str,
    status: str,
    subject: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            authored=authored,
            based_on=based_on,
            category=category,
            encounter=encounter,
            group_identifier=group_identifier,
            identifier=identifier,
            medium=medium,
            occurrence=occurrence,
            patient=patient,
            priority=priority,
            recipient=recipient,
            replaces=replaces,
            requester=requester,
            sender=sender,
            status=status,
            subject=subject,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def compartmentdefinition_search(
    request: Request,
    response: Response,
    code: str,
    context: str,
    context_quantity: str,
    context_type: str,
    context_type_quantity: str,
    context_type_value: str,
    date: str,
    description: str,
    name: str,
    publisher: str,
    resource: str,
    status: str,
    url: str,
    version: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            code=code,
            context=context,
            context_quantity=context_quantity,
            context_type=context_type,
            context_type_quantity=context_type_quantity,
            context_type_value=context_type_value,
            date=date,
            description=description,
            name=name,
            publisher=publisher,
            resource=resource,
            status=status,
            url=url,
            version=version,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def composition_search(
    request: Request,
    response: Response,
    attester: str,
    author: str,
    category: str,
    confidentiality: str,
    context: str,
    date: str,
    encounter: str,
    entry: str,
    identifier: str,
    patient: str,
    period: str,
    related_id: str,
    related_ref: str,
    section: str,
    status: str,
    subject: str,
    title: str,
    type_: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            attester=attester,
            author=author,
            category=category,
            confidentiality=confidentiality,
            context=context,
            date=date,
            encounter=encounter,
            entry=entry,
            identifier=identifier,
            patient=patient,
            period=period,
            related_id=related_id,
            related_ref=related_ref,
            section=section,
            status=status,
            subject=subject,
            title=title,
            type_=type_,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def conceptmap_search(
    request: Request,
    response: Response,
    context: str,
    context_quantity: str,
    context_type: str,
    context_type_quantity: str,
    context_type_value: str,
    date: str,
    dependson: str,
    description: str,
    identifier: str,
    jurisdiction: str,
    name: str,
    other: str,
    product: str,
    publisher: str,
    source: str,
    source_code: str,
    source_system: str,
    source_uri: str,
    status: str,
    target: str,
    target_code: str,
    target_system: str,
    target_uri: str,
    title: str,
    url: str,
    version: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            context=context,
            context_quantity=context_quantity,
            context_type=context_type,
            context_type_quantity=context_type_quantity,
            context_type_value=context_type_value,
            date=date,
            dependson=dependson,
            description=description,
            identifier=identifier,
            jurisdiction=jurisdiction,
            name=name,
            other=other,
            product=product,
            publisher=publisher,
            source=source,
            source_code=source_code,
            source_system=source_system,
            source_uri=source_uri,
            status=status,
            target=target,
            target_code=target_code,
            target_system=target_system,
            target_uri=target_uri,
            title=title,
            url=url,
            version=version,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def condition_search(
    request: Request,
    response: Response,
    abatement_age: str,
    abatement_date: str,
    abatement_string: str,
    asserter: str,
    body_site: str,
    category: str,
    clinical_status: str,
    code: str,
    encounter: str,
    evidence: str,
    evidence_detail: str,
    identifier: str,
    onset_age: str,
    onset_date: str,
    onset_info: str,
    patient: str,
    recorded_date: str,
    severity: str,
    stage: str,
    subject: str,
    verification_status: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            abatement_age=abatement_age,
            abatement_date=abatement_date,
            abatement_string=abatement_string,
            asserter=asserter,
            body_site=body_site,
            category=category,
            clinical_status=clinical_status,
            code=code,
            encounter=encounter,
            evidence=evidence,
            evidence_detail=evidence_detail,
            identifier=identifier,
            onset_age=onset_age,
            onset_date=onset_date,
            onset_info=onset_info,
            patient=patient,
            recorded_date=recorded_date,
            severity=severity,
            stage=stage,
            subject=subject,
            verification_status=verification_status,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def consent_search(
    request: Request,
    response: Response,
    action: str,
    actor: str,
    category: str,
    consentor: str,
    data: str,
    date: str,
    identifier: str,
    organization: str,
    patient: str,
    period: str,
    purpose: str,
    scope: str,
    security_label: str,
    source_reference: str,
    status: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            action=action,
            actor=actor,
            category=category,
            consentor=consentor,
            data=data,
            date=date,
            identifier=identifier,
            organization=organization,
            patient=patient,
            period=period,
            purpose=purpose,
            scope=scope,
            security_label=security_label,
            source_reference=source_reference,
            status=status,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def contract_search(
    request: Request,
    response: Response,
    authority: str,
    domain: str,
    identifier: str,
    instantiates: str,
    issued: str,
    patient: str,
    signer: str,
    status: str,
    subject: str,
    url: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            authority=authority,
            domain=domain,
            identifier=identifier,
            instantiates=instantiates,
            issued=issued,
            patient=patient,
            signer=signer,
            status=status,
            subject=subject,
            url=url,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def coverage_search(
    request: Request,
    response: Response,
    beneficiary: str,
    class_type: str,
    class_value: str,
    dependent: str,
    identifier: str,
    patient: str,
    payor: str,
    policy_holder: str,
    status: str,
    subscriber: str,
    type_: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            beneficiary=beneficiary,
            class_type=class_type,
            class_value=class_value,
            dependent=dependent,
            identifier=identifier,
            patient=patient,
            payor=payor,
            policy_holder=policy_holder,
            status=status,
            subscriber=subscriber,
            type_=type_,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def coverageeligibilityrequest_search(
    request: Request,
    response: Response,
    created: str,
    enterer: str,
    facility: str,
    identifier: str,
    patient: str,
    provider: str,
    status: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            created=created,
            enterer=enterer,
            facility=facility,
            identifier=identifier,
            patient=patient,
            provider=provider,
            status=status,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def coverageeligibilityresponse_search(
    request: Request,
    response: Response,
    created: str,
    disposition: str,
    identifier: str,
    insurer: str,
    outcome: str,
    patient: str,
    request_: str,
    requestor: str,
    status: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            created=created,
            disposition=disposition,
            identifier=identifier,
            insurer=insurer,
            outcome=outcome,
            patient=patient,
            request_=request_,
            requestor=requestor,
            status=status,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def detectedissue_search(
    request: Request,
    response: Response,
    author: str,
    code: str,
    identified: str,
    identifier: str,
    implicated: str,
    patient: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            author=author,
            code=code,
            identified=identified,
            identifier=identifier,
            implicated=implicated,
            patient=patient,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def device_search(
    request: Request,
    response: Response,
    device_name: str,
    identifier: str,
    location: str,
    manufacturer: str,
    model: str,
    organization: str,
    patient: str,
    status: str,
    type_: str,
    udi_carrier: str,
    udi_di: str,
    url: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            device_name=device_name,
            identifier=identifier,
            location=location,
            manufacturer=manufacturer,
            model=model,
            organization=organization,
            patient=patient,
            status=status,
            type_=type_,
            udi_carrier=udi_carrier,
            udi_di=udi_di,
            url=url,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def devicedefinition_search(
    request: Request, response: Response, identifier: str, parent: str, type_: str
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(identifier=identifier, parent=parent, type_=type_),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def devicemetric_search(
    request: Request,
    response: Response,
    category: str,
    identifier: str,
    parent: str,
    source: str,
    type_: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            category=category,
            identifier=identifier,
            parent=parent,
            source=source,
            type_=type_,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def devicerequest_search(
    request: Request,
    response: Response,
    authored_on: str,
    based_on: str,
    code: str,
    device: str,
    encounter: str,
    event_date: str,
    group_identifier: str,
    identifier: str,
    instantiates_canonical: str,
    instantiates_uri: str,
    insurance: str,
    intent: str,
    patient: str,
    performer: str,
    prior_request: str,
    requester: str,
    status: str,
    subject: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            authored_on=authored_on,
            based_on=based_on,
            code=code,
            device=device,
            encounter=encounter,
            event_date=event_date,
            group_identifier=group_identifier,
            identifier=identifier,
            instantiates_canonical=instantiates_canonical,
            instantiates_uri=instantiates_uri,
            insurance=insurance,
            intent=intent,
            patient=patient,
            performer=performer,
            prior_request=prior_request,
            requester=requester,
            status=status,
            subject=subject,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def deviceusestatement_search(
    request: Request,
    response: Response,
    device: str,
    identifier: str,
    patient: str,
    subject: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            device=device, identifier=identifier, patient=patient, subject=subject
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def diagnosticreport_search(
    request: Request,
    response: Response,
    based_on: str,
    category: str,
    code: str,
    conclusion: str,
    date: str,
    encounter: str,
    identifier: str,
    issued: str,
    media: str,
    patient: str,
    performer: str,
    result_: str,
    results_interpreter: str,
    specimen: str,
    status: str,
    subject: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            based_on=based_on,
            category=category,
            code=code,
            conclusion=conclusion,
            date=date,
            encounter=encounter,
            identifier=identifier,
            issued=issued,
            media=media,
            patient=patient,
            performer=performer,
            result_=result_,
            results_interpreter=results_interpreter,
            specimen=specimen,
            status=status,
            subject=subject,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def documentmanifest_search(
    request: Request,
    response: Response,
    author: str,
    created: str,
    description: str,
    identifier: str,
    item: str,
    patient: str,
    recipient: str,
    related_id: str,
    related_ref: str,
    source: str,
    status: str,
    subject: str,
    type_: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            author=author,
            created=created,
            description=description,
            identifier=identifier,
            item=item,
            patient=patient,
            recipient=recipient,
            related_id=related_id,
            related_ref=related_ref,
            source=source,
            status=status,
            subject=subject,
            type_=type_,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def documentreference_search(
    request: Request,
    response: Response,
    authenticator: str,
    author: str,
    category: str,
    contenttype: str,
    custodian: str,
    date: str,
    description: str,
    encounter: str,
    event: str,
    facility: str,
    format_: str,
    identifier: str,
    language: str,
    location: str,
    patient: str,
    period: str,
    related: str,
    relatesto: str,
    relation: str,
    relationship: str,
    security_label: str,
    setting: str,
    status: str,
    subject: str,
    type_: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            authenticator=authenticator,
            author=author,
            category=category,
            contenttype=contenttype,
            custodian=custodian,
            date=date,
            description=description,
            encounter=encounter,
            event=event,
            facility=facility,
            format_=format_,
            identifier=identifier,
            language=language,
            location=location,
            patient=patient,
            period=period,
            related=related,
            relatesto=relatesto,
            relation=relation,
            relationship=relationship,
            security_label=security_label,
            setting=setting,
            status=status,
            subject=subject,
            type_=type_,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def effectevidencesynthesis_search(
    request: Request,
    response: Response,
    context: str,
    context_quantity: str,
    context_type: str,
    context_type_quantity: str,
    context_type_value: str,
    date: str,
    description: str,
    effective: str,
    identifier: str,
    jurisdiction: str,
    name: str,
    publisher: str,
    status: str,
    title: str,
    url: str,
    version: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            context=context,
            context_quantity=context_quantity,
            context_type=context_type,
            context_type_quantity=context_type_quantity,
            context_type_value=context_type_value,
            date=date,
            description=description,
            effective=effective,
            identifier=identifier,
            jurisdiction=jurisdiction,
            name=name,
            publisher=publisher,
            status=status,
            title=title,
            url=url,
            version=version,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def encounter_search(
    request: Request,
    response: Response,
    account: str,
    appointment: str,
    based_on: str,
    class_: str,
    date: str,
    diagnosis: str,
    episode_of_care: str,
    identifier: str,
    length: str,
    location: str,
    location_period: str,
    part_of: str,
    participant: str,
    participant_type: str,
    patient: str,
    practitioner: str,
    reason_code: str,
    reason_reference: str,
    service_provider: str,
    special_arrangement: str,
    status: str,
    subject: str,
    type_: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            account=account,
            appointment=appointment,
            based_on=based_on,
            class_=class_,
            date=date,
            diagnosis=diagnosis,
            episode_of_care=episode_of_care,
            identifier=identifier,
            length=length,
            location=location,
            location_period=location_period,
            part_of=part_of,
            participant=participant,
            participant_type=participant_type,
            patient=patient,
            practitioner=practitioner,
            reason_code=reason_code,
            reason_reference=reason_reference,
            service_provider=service_provider,
            special_arrangement=special_arrangement,
            status=status,
            subject=subject,
            type_=type_,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def endpoint_search(
    request: Request,
    response: Response,
    connection_type: str,
    identifier: str,
    name: str,
    organization: str,
    payload_type: str,
    status: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            connection_type=connection_type,
            identifier=identifier,
            name=name,
            organization=organization,
            payload_type=payload_type,
            status=status,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def enrollmentrequest_search(
    request: Request,
    response: Response,
    identifier: str,
    patient: str,
    status: str,
    subject: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            identifier=identifier, patient=patient, status=status, subject=subject
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def enrollmentresponse_search(
    request: Request, response: Response, identifier: str, request_: str, status: str
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(identifier=identifier, request_=request_, status=status),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def episodeofcare_search(
    request: Request,
    response: Response,
    care_manager: str,
    condition: str,
    date: str,
    identifier: str,
    incoming_referral: str,
    organization: str,
    patient: str,
    status: str,
    type_: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            care_manager=care_manager,
            condition=condition,
            date=date,
            identifier=identifier,
            incoming_referral=incoming_referral,
            organization=organization,
            patient=patient,
            status=status,
            type_=type_,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def eventdefinition_search(
    request: Request,
    response: Response,
    composed_of: str,
    context: str,
    context_quantity: str,
    context_type: str,
    context_type_quantity: str,
    context_type_value: str,
    date: str,
    depends_on: str,
    derived_from: str,
    description: str,
    effective: str,
    identifier: str,
    jurisdiction: str,
    name: str,
    predecessor: str,
    publisher: str,
    status: str,
    successor: str,
    title: str,
    topic: str,
    url: str,
    version: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            composed_of=composed_of,
            context=context,
            context_quantity=context_quantity,
            context_type=context_type,
            context_type_quantity=context_type_quantity,
            context_type_value=context_type_value,
            date=date,
            depends_on=depends_on,
            derived_from=derived_from,
            description=description,
            effective=effective,
            identifier=identifier,
            jurisdiction=jurisdiction,
            name=name,
            predecessor=predecessor,
            publisher=publisher,
            status=status,
            successor=successor,
            title=title,
            topic=topic,
            url=url,
            version=version,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def evidence_search(
    request: Request,
    response: Response,
    composed_of: str,
    context: str,
    context_quantity: str,
    context_type: str,
    context_type_quantity: str,
    context_type_value: str,
    date: str,
    depends_on: str,
    derived_from: str,
    description: str,
    effective: str,
    identifier: str,
    jurisdiction: str,
    name: str,
    predecessor: str,
    publisher: str,
    status: str,
    successor: str,
    title: str,
    topic: str,
    url: str,
    version: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            composed_of=composed_of,
            context=context,
            context_quantity=context_quantity,
            context_type=context_type,
            context_type_quantity=context_type_quantity,
            context_type_value=context_type_value,
            date=date,
            depends_on=depends_on,
            derived_from=derived_from,
            description=description,
            effective=effective,
            identifier=identifier,
            jurisdiction=jurisdiction,
            name=name,
            predecessor=predecessor,
            publisher=publisher,
            status=status,
            successor=successor,
            title=title,
            topic=topic,
            url=url,
            version=version,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def evidencevariable_search(
    request: Request,
    response: Response,
    composed_of: str,
    context: str,
    context_quantity: str,
    context_type: str,
    context_type_quantity: str,
    context_type_value: str,
    date: str,
    depends_on: str,
    derived_from: str,
    description: str,
    effective: str,
    identifier: str,
    jurisdiction: str,
    name: str,
    predecessor: str,
    publisher: str,
    status: str,
    successor: str,
    title: str,
    topic: str,
    url: str,
    version: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            composed_of=composed_of,
            context=context,
            context_quantity=context_quantity,
            context_type=context_type,
            context_type_quantity=context_type_quantity,
            context_type_value=context_type_value,
            date=date,
            depends_on=depends_on,
            derived_from=derived_from,
            description=description,
            effective=effective,
            identifier=identifier,
            jurisdiction=jurisdiction,
            name=name,
            predecessor=predecessor,
            publisher=publisher,
            status=status,
            successor=successor,
            title=title,
            topic=topic,
            url=url,
            version=version,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def examplescenario_search(
    request: Request,
    response: Response,
    context: str,
    context_quantity: str,
    context_type: str,
    context_type_quantity: str,
    context_type_value: str,
    date: str,
    identifier: str,
    jurisdiction: str,
    name: str,
    publisher: str,
    status: str,
    url: str,
    version: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            context=context,
            context_quantity=context_quantity,
            context_type=context_type,
            context_type_quantity=context_type_quantity,
            context_type_value=context_type_value,
            date=date,
            identifier=identifier,
            jurisdiction=jurisdiction,
            name=name,
            publisher=publisher,
            status=status,
            url=url,
            version=version,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def explanationofbenefit_search(
    request: Request,
    response: Response,
    care_team: str,
    claim: str,
    coverage: str,
    created: str,
    detail_udi: str,
    disposition: str,
    encounter: str,
    enterer: str,
    facility: str,
    identifier: str,
    item_udi: str,
    patient: str,
    payee: str,
    procedure_udi: str,
    provider: str,
    status: str,
    subdetail_udi: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            care_team=care_team,
            claim=claim,
            coverage=coverage,
            created=created,
            detail_udi=detail_udi,
            disposition=disposition,
            encounter=encounter,
            enterer=enterer,
            facility=facility,
            identifier=identifier,
            item_udi=item_udi,
            patient=patient,
            payee=payee,
            procedure_udi=procedure_udi,
            provider=provider,
            status=status,
            subdetail_udi=subdetail_udi,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def familymemberhistory_search(
    request: Request,
    response: Response,
    code: str,
    date: str,
    identifier: str,
    instantiates_canonical: str,
    instantiates_uri: str,
    patient: str,
    relationship: str,
    sex: str,
    status: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            code=code,
            date=date,
            identifier=identifier,
            instantiates_canonical=instantiates_canonical,
            instantiates_uri=instantiates_uri,
            patient=patient,
            relationship=relationship,
            sex=sex,
            status=status,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def flag_search(
    request: Request,
    response: Response,
    author: str,
    date: str,
    encounter: str,
    identifier: str,
    patient: str,
    subject: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            author=author,
            date=date,
            encounter=encounter,
            identifier=identifier,
            patient=patient,
            subject=subject,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def goal_search(
    request: Request,
    response: Response,
    achievement_status: str,
    category: str,
    identifier: str,
    lifecycle_status: str,
    patient: str,
    start_date: str,
    subject: str,
    target_date: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            achievement_status=achievement_status,
            category=category,
            identifier=identifier,
            lifecycle_status=lifecycle_status,
            patient=patient,
            start_date=start_date,
            subject=subject,
            target_date=target_date,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def graphdefinition_search(
    request: Request,
    response: Response,
    context: str,
    context_quantity: str,
    context_type: str,
    context_type_quantity: str,
    context_type_value: str,
    date: str,
    description: str,
    jurisdiction: str,
    name: str,
    publisher: str,
    start: str,
    status: str,
    url: str,
    version: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            context=context,
            context_quantity=context_quantity,
            context_type=context_type,
            context_type_quantity=context_type_quantity,
            context_type_value=context_type_value,
            date=date,
            description=description,
            jurisdiction=jurisdiction,
            name=name,
            publisher=publisher,
            start=start,
            status=status,
            url=url,
            version=version,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def group_search(
    request: Request,
    response: Response,
    actual: str,
    characteristic: str,
    characteristic_value: str,
    code: str,
    exclude: str,
    identifier: str,
    managing_entity: str,
    member: str,
    type_: str,
    value: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            actual=actual,
            characteristic=characteristic,
            characteristic_value=characteristic_value,
            code=code,
            exclude=exclude,
            identifier=identifier,
            managing_entity=managing_entity,
            member=member,
            type_=type_,
            value=value,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def guidanceresponse_search(
    request: Request,
    response: Response,
    identifier: str,
    patient: str,
    request_: str,
    subject: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            identifier=identifier, patient=patient, request_=request_, subject=subject
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def healthcareservice_search(
    request: Request,
    response: Response,
    active: str,
    characteristic: str,
    coverage_area: str,
    endpoint: str,
    identifier: str,
    location: str,
    name: str,
    organization: str,
    program: str,
    service_category: str,
    service_type: str,
    specialty: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            active=active,
            characteristic=characteristic,
            coverage_area=coverage_area,
            endpoint=endpoint,
            identifier=identifier,
            location=location,
            name=name,
            organization=organization,
            program=program,
            service_category=service_category,
            service_type=service_type,
            specialty=specialty,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def imagingstudy_search(
    request: Request,
    response: Response,
    basedon: str,
    bodysite: str,
    dicom_class: str,
    encounter: str,
    endpoint: str,
    identifier: str,
    instance: str,
    interpreter: str,
    modality: str,
    patient: str,
    performer: str,
    reason: str,
    referrer: str,
    series: str,
    started: str,
    status: str,
    subject: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            basedon=basedon,
            bodysite=bodysite,
            dicom_class=dicom_class,
            encounter=encounter,
            endpoint=endpoint,
            identifier=identifier,
            instance=instance,
            interpreter=interpreter,
            modality=modality,
            patient=patient,
            performer=performer,
            reason=reason,
            referrer=referrer,
            series=series,
            started=started,
            status=status,
            subject=subject,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def immunization_search(
    request: Request,
    response: Response,
    date: str,
    identifier: str,
    location: str,
    lot_number: str,
    manufacturer: str,
    patient: str,
    performer: str,
    reaction: str,
    reaction_date: str,
    reason_code: str,
    reason_reference: str,
    series: str,
    status: str,
    status_reason: str,
    target_disease: str,
    vaccine_code: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            date=date,
            identifier=identifier,
            location=location,
            lot_number=lot_number,
            manufacturer=manufacturer,
            patient=patient,
            performer=performer,
            reaction=reaction,
            reaction_date=reaction_date,
            reason_code=reason_code,
            reason_reference=reason_reference,
            series=series,
            status=status,
            status_reason=status_reason,
            target_disease=target_disease,
            vaccine_code=vaccine_code,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def immunizationevaluation_search(
    request: Request,
    response: Response,
    date: str,
    dose_status: str,
    identifier: str,
    immunization_event: str,
    patient: str,
    status: str,
    target_disease: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            date=date,
            dose_status=dose_status,
            identifier=identifier,
            immunization_event=immunization_event,
            patient=patient,
            status=status,
            target_disease=target_disease,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def immunizationrecommendation_search(
    request: Request,
    response: Response,
    date: str,
    identifier: str,
    information: str,
    patient: str,
    status: str,
    support: str,
    target_disease: str,
    vaccine_type: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            date=date,
            identifier=identifier,
            information=information,
            patient=patient,
            status=status,
            support=support,
            target_disease=target_disease,
            vaccine_type=vaccine_type,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def implementationguide_search(
    request: Request,
    response: Response,
    context: str,
    context_quantity: str,
    context_type: str,
    context_type_quantity: str,
    context_type_value: str,
    date: str,
    depends_on: str,
    description: str,
    experimental: str,
    global_: str,
    jurisdiction: str,
    name: str,
    publisher: str,
    resource: str,
    status: str,
    title: str,
    url: str,
    version: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            context=context,
            context_quantity=context_quantity,
            context_type=context_type,
            context_type_quantity=context_type_quantity,
            context_type_value=context_type_value,
            date=date,
            depends_on=depends_on,
            description=description,
            experimental=experimental,
            global_=global_,
            jurisdiction=jurisdiction,
            name=name,
            publisher=publisher,
            resource=resource,
            status=status,
            title=title,
            url=url,
            version=version,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def insuranceplan_search(
    request: Request,
    response: Response,
    address: str,
    address_city: str,
    address_country: str,
    address_postalcode: str,
    address_state: str,
    address_use: str,
    administered_by: str,
    endpoint: str,
    identifier: str,
    name: str,
    owned_by: str,
    phonetic: str,
    status: str,
    type_: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            address=address,
            address_city=address_city,
            address_country=address_country,
            address_postalcode=address_postalcode,
            address_state=address_state,
            address_use=address_use,
            administered_by=administered_by,
            endpoint=endpoint,
            identifier=identifier,
            name=name,
            owned_by=owned_by,
            phonetic=phonetic,
            status=status,
            type_=type_,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def invoice_search(
    request: Request,
    response: Response,
    account: str,
    date: str,
    identifier: str,
    issuer: str,
    participant: str,
    participant_role: str,
    patient: str,
    recipient: str,
    status: str,
    subject: str,
    totalgross: str,
    totalnet: str,
    type_: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            account=account,
            date=date,
            identifier=identifier,
            issuer=issuer,
            participant=participant,
            participant_role=participant_role,
            patient=patient,
            recipient=recipient,
            status=status,
            subject=subject,
            totalgross=totalgross,
            totalnet=totalnet,
            type_=type_,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def library_search(
    request: Request,
    response: Response,
    composed_of: str,
    content_type: str,
    context: str,
    context_quantity: str,
    context_type: str,
    context_type_quantity: str,
    context_type_value: str,
    date: str,
    depends_on: str,
    derived_from: str,
    description: str,
    effective: str,
    identifier: str,
    jurisdiction: str,
    name: str,
    predecessor: str,
    publisher: str,
    status: str,
    successor: str,
    title: str,
    topic: str,
    type_: str,
    url: str,
    version: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            composed_of=composed_of,
            content_type=content_type,
            context=context,
            context_quantity=context_quantity,
            context_type=context_type,
            context_type_quantity=context_type_quantity,
            context_type_value=context_type_value,
            date=date,
            depends_on=depends_on,
            derived_from=derived_from,
            description=description,
            effective=effective,
            identifier=identifier,
            jurisdiction=jurisdiction,
            name=name,
            predecessor=predecessor,
            publisher=publisher,
            status=status,
            successor=successor,
            title=title,
            topic=topic,
            type_=type_,
            url=url,
            version=version,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def linkage_search(
    request: Request, response: Response, author: str, item: str, source: str
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(author=author, item=item, source=source),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def list_search(
    request: Request,
    response: Response,
    code: str,
    date: str,
    empty_reason: str,
    encounter: str,
    identifier: str,
    item: str,
    notes: str,
    patient: str,
    source: str,
    status: str,
    subject: str,
    title: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            code=code,
            date=date,
            empty_reason=empty_reason,
            encounter=encounter,
            identifier=identifier,
            item=item,
            notes=notes,
            patient=patient,
            source=source,
            status=status,
            subject=subject,
            title=title,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def location_search(
    request: Request,
    response: Response,
    address: str,
    address_city: str,
    address_country: str,
    address_postalcode: str,
    address_state: str,
    address_use: str,
    endpoint: str,
    identifier: str,
    name: str,
    near: str,
    operational_status: str,
    organization: str,
    partof: str,
    status: str,
    type_: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            address=address,
            address_city=address_city,
            address_country=address_country,
            address_postalcode=address_postalcode,
            address_state=address_state,
            address_use=address_use,
            endpoint=endpoint,
            identifier=identifier,
            name=name,
            near=near,
            operational_status=operational_status,
            organization=organization,
            partof=partof,
            status=status,
            type_=type_,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def measure_search(
    request: Request,
    response: Response,
    composed_of: str,
    context: str,
    context_quantity: str,
    context_type: str,
    context_type_quantity: str,
    context_type_value: str,
    date: str,
    depends_on: str,
    derived_from: str,
    description: str,
    effective: str,
    identifier: str,
    jurisdiction: str,
    name: str,
    predecessor: str,
    publisher: str,
    status: str,
    successor: str,
    title: str,
    topic: str,
    url: str,
    version: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            composed_of=composed_of,
            context=context,
            context_quantity=context_quantity,
            context_type=context_type,
            context_type_quantity=context_type_quantity,
            context_type_value=context_type_value,
            date=date,
            depends_on=depends_on,
            derived_from=derived_from,
            description=description,
            effective=effective,
            identifier=identifier,
            jurisdiction=jurisdiction,
            name=name,
            predecessor=predecessor,
            publisher=publisher,
            status=status,
            successor=successor,
            title=title,
            topic=topic,
            url=url,
            version=version,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def measurereport_search(
    request: Request,
    response: Response,
    date: str,
    evaluated_resource: str,
    identifier: str,
    measure: str,
    patient: str,
    period: str,
    reporter: str,
    status: str,
    subject: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            date=date,
            evaluated_resource=evaluated_resource,
            identifier=identifier,
            measure=measure,
            patient=patient,
            period=period,
            reporter=reporter,
            status=status,
            subject=subject,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def media_search(
    request: Request,
    response: Response,
    based_on: str,
    created: str,
    device: str,
    encounter: str,
    identifier: str,
    modality: str,
    operator: str,
    patient: str,
    site: str,
    status: str,
    subject: str,
    type_: str,
    view: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            based_on=based_on,
            created=created,
            device=device,
            encounter=encounter,
            identifier=identifier,
            modality=modality,
            operator=operator,
            patient=patient,
            site=site,
            status=status,
            subject=subject,
            type_=type_,
            view=view,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def medication_search(
    request: Request,
    response: Response,
    code: str,
    expiration_date: str,
    form: str,
    identifier: str,
    ingredient: str,
    ingredient_code: str,
    lot_number: str,
    manufacturer: str,
    status: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            code=code,
            expiration_date=expiration_date,
            form=form,
            identifier=identifier,
            ingredient=ingredient,
            ingredient_code=ingredient_code,
            lot_number=lot_number,
            manufacturer=manufacturer,
            status=status,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def medicationadministration_search(
    request: Request,
    response: Response,
    code: str,
    context: str,
    device: str,
    effective_time: str,
    identifier: str,
    medication: str,
    patient: str,
    performer: str,
    reason_given: str,
    reason_not_given: str,
    request_: str,
    status: str,
    subject: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            code=code,
            context=context,
            device=device,
            effective_time=effective_time,
            identifier=identifier,
            medication=medication,
            patient=patient,
            performer=performer,
            reason_given=reason_given,
            reason_not_given=reason_not_given,
            request_=request_,
            status=status,
            subject=subject,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def medicationdispense_search(
    request: Request,
    response: Response,
    code: str,
    context: str,
    destination: str,
    identifier: str,
    medication: str,
    patient: str,
    performer: str,
    prescription: str,
    receiver: str,
    responsibleparty: str,
    status: str,
    subject: str,
    type_: str,
    whenhandedover: str,
    whenprepared: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            code=code,
            context=context,
            destination=destination,
            identifier=identifier,
            medication=medication,
            patient=patient,
            performer=performer,
            prescription=prescription,
            receiver=receiver,
            responsibleparty=responsibleparty,
            status=status,
            subject=subject,
            type_=type_,
            whenhandedover=whenhandedover,
            whenprepared=whenprepared,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def medicationknowledge_search(
    request: Request,
    response: Response,
    classification: str,
    classification_type: str,
    code: str,
    doseform: str,
    ingredient: str,
    ingredient_code: str,
    manufacturer: str,
    monitoring_program_name: str,
    monitoring_program_type: str,
    monograph: str,
    monograph_type: str,
    source_cost: str,
    status: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            classification=classification,
            classification_type=classification_type,
            code=code,
            doseform=doseform,
            ingredient=ingredient,
            ingredient_code=ingredient_code,
            manufacturer=manufacturer,
            monitoring_program_name=monitoring_program_name,
            monitoring_program_type=monitoring_program_type,
            monograph=monograph,
            monograph_type=monograph_type,
            source_cost=source_cost,
            status=status,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def medicationrequest_search(
    request: Request,
    response: Response,
    authoredon: str,
    category: str,
    code: str,
    date: str,
    encounter: str,
    identifier: str,
    intended_dispenser: str,
    intended_performer: str,
    intended_performertype: str,
    intent: str,
    medication: str,
    patient: str,
    priority: str,
    requester: str,
    status: str,
    subject: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            authoredon=authoredon,
            category=category,
            code=code,
            date=date,
            encounter=encounter,
            identifier=identifier,
            intended_dispenser=intended_dispenser,
            intended_performer=intended_performer,
            intended_performertype=intended_performertype,
            intent=intent,
            medication=medication,
            patient=patient,
            priority=priority,
            requester=requester,
            status=status,
            subject=subject,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def medicationstatement_search(
    request: Request,
    response: Response,
    category: str,
    code: str,
    context: str,
    effective: str,
    identifier: str,
    medication: str,
    part_of: str,
    patient: str,
    source: str,
    status: str,
    subject: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            category=category,
            code=code,
            context=context,
            effective=effective,
            identifier=identifier,
            medication=medication,
            part_of=part_of,
            patient=patient,
            source=source,
            status=status,
            subject=subject,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def medicinalproduct_search(
    request: Request, response: Response, identifier: str, name: str, name_language: str
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(identifier=identifier, name=name, name_language=name_language),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def medicinalproductauthorization_search(
    request: Request,
    response: Response,
    country: str,
    holder: str,
    identifier: str,
    status: str,
    subject: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            country=country,
            holder=holder,
            identifier=identifier,
            status=status,
            subject=subject,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def medicinalproductcontraindication_search(
    request: Request, response: Response, subject: str
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType], await callable_(subject=subject)
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def medicinalproductindication_search(
    request: Request, response: Response, subject: str
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType], await callable_(subject=subject)
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def medicinalproductinteraction_search(
    request: Request, response: Response, subject: str
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType], await callable_(subject=subject)
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def medicinalproductpackaged_search(
    request: Request, response: Response, identifier: str, subject: str
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(identifier=identifier, subject=subject),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def medicinalproductpharmaceutical_search(
    request: Request,
    response: Response,
    identifier: str,
    route: str,
    target_species: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            identifier=identifier, route=route, target_species=target_species
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def medicinalproductundesirableeffect_search(
    request: Request, response: Response, subject: str
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType], await callable_(subject=subject)
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def messagedefinition_search(
    request: Request,
    response: Response,
    category: str,
    context: str,
    context_quantity: str,
    context_type: str,
    context_type_quantity: str,
    context_type_value: str,
    date: str,
    description: str,
    event: str,
    focus: str,
    identifier: str,
    jurisdiction: str,
    name: str,
    parent: str,
    publisher: str,
    status: str,
    title: str,
    url: str,
    version: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            category=category,
            context=context,
            context_quantity=context_quantity,
            context_type=context_type,
            context_type_quantity=context_type_quantity,
            context_type_value=context_type_value,
            date=date,
            description=description,
            event=event,
            focus=focus,
            identifier=identifier,
            jurisdiction=jurisdiction,
            name=name,
            parent=parent,
            publisher=publisher,
            status=status,
            title=title,
            url=url,
            version=version,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def messageheader_search(
    request: Request,
    response: Response,
    author: str,
    code: str,
    destination: str,
    destination_uri: str,
    enterer: str,
    event: str,
    focus: str,
    receiver: str,
    response_id: str,
    responsible: str,
    sender: str,
    source: str,
    source_uri: str,
    target: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            author=author,
            code=code,
            destination=destination,
            destination_uri=destination_uri,
            enterer=enterer,
            event=event,
            focus=focus,
            receiver=receiver,
            response_id=response_id,
            responsible=responsible,
            sender=sender,
            source=source,
            source_uri=source_uri,
            target=target,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def molecularsequence_search(
    request: Request,
    response: Response,
    chromosome: str,
    chromosome_variant_coordinate: str,
    chromosome_window_coordinate: str,
    identifier: str,
    patient: str,
    referenceseqid: str,
    referenceseqid_variant_coordinate: str,
    referenceseqid_window_coordinate: str,
    type_: str,
    variant_end: str,
    variant_start: str,
    window_end: str,
    window_start: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            chromosome=chromosome,
            chromosome_variant_coordinate=chromosome_variant_coordinate,
            chromosome_window_coordinate=chromosome_window_coordinate,
            identifier=identifier,
            patient=patient,
            referenceseqid=referenceseqid,
            referenceseqid_variant_coordinate=referenceseqid_variant_coordinate,
            referenceseqid_window_coordinate=referenceseqid_window_coordinate,
            type_=type_,
            variant_end=variant_end,
            variant_start=variant_start,
            window_end=window_end,
            window_start=window_start,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def namingsystem_search(
    request: Request,
    response: Response,
    contact: str,
    context: str,
    context_quantity: str,
    context_type: str,
    context_type_quantity: str,
    context_type_value: str,
    date: str,
    description: str,
    id_type: str,
    jurisdiction: str,
    kind: str,
    name: str,
    period: str,
    publisher: str,
    responsible: str,
    status: str,
    telecom: str,
    type_: str,
    value: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            contact=contact,
            context=context,
            context_quantity=context_quantity,
            context_type=context_type,
            context_type_quantity=context_type_quantity,
            context_type_value=context_type_value,
            date=date,
            description=description,
            id_type=id_type,
            jurisdiction=jurisdiction,
            kind=kind,
            name=name,
            period=period,
            publisher=publisher,
            responsible=responsible,
            status=status,
            telecom=telecom,
            type_=type_,
            value=value,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def nutritionorder_search(
    request: Request,
    response: Response,
    additive: str,
    datetime: str,
    encounter: str,
    formula: str,
    identifier: str,
    instantiates_canonical: str,
    instantiates_uri: str,
    oraldiet: str,
    patient: str,
    provider: str,
    status: str,
    supplement: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            additive=additive,
            datetime=datetime,
            encounter=encounter,
            formula=formula,
            identifier=identifier,
            instantiates_canonical=instantiates_canonical,
            instantiates_uri=instantiates_uri,
            oraldiet=oraldiet,
            patient=patient,
            provider=provider,
            status=status,
            supplement=supplement,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def observation_search(
    request: Request,
    response: Response,
    based_on: str,
    category: str,
    code: str,
    code_value_concept: str,
    code_value_date: str,
    code_value_quantity: str,
    code_value_string: str,
    combo_code: str,
    combo_code_value_concept: str,
    combo_code_value_quantity: str,
    combo_data_absent_reason: str,
    combo_value_concept: str,
    combo_value_quantity: str,
    component_code: str,
    component_code_value_concept: str,
    component_code_value_quantity: str,
    component_data_absent_reason: str,
    component_value_concept: str,
    component_value_quantity: str,
    data_absent_reason: str,
    date: str,
    derived_from: str,
    device: str,
    encounter: str,
    focus: str,
    has_member: str,
    identifier: str,
    method: str,
    part_of: str,
    patient: str,
    performer: str,
    specimen: str,
    status: str,
    subject: str,
    value_concept: str,
    value_date: str,
    value_quantity: str,
    value_string: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            based_on=based_on,
            category=category,
            code=code,
            code_value_concept=code_value_concept,
            code_value_date=code_value_date,
            code_value_quantity=code_value_quantity,
            code_value_string=code_value_string,
            combo_code=combo_code,
            combo_code_value_concept=combo_code_value_concept,
            combo_code_value_quantity=combo_code_value_quantity,
            combo_data_absent_reason=combo_data_absent_reason,
            combo_value_concept=combo_value_concept,
            combo_value_quantity=combo_value_quantity,
            component_code=component_code,
            component_code_value_concept=component_code_value_concept,
            component_code_value_quantity=component_code_value_quantity,
            component_data_absent_reason=component_data_absent_reason,
            component_value_concept=component_value_concept,
            component_value_quantity=component_value_quantity,
            data_absent_reason=data_absent_reason,
            date=date,
            derived_from=derived_from,
            device=device,
            encounter=encounter,
            focus=focus,
            has_member=has_member,
            identifier=identifier,
            method=method,
            part_of=part_of,
            patient=patient,
            performer=performer,
            specimen=specimen,
            status=status,
            subject=subject,
            value_concept=value_concept,
            value_date=value_date,
            value_quantity=value_quantity,
            value_string=value_string,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def operationdefinition_search(
    request: Request,
    response: Response,
    base: str,
    code: str,
    context: str,
    context_quantity: str,
    context_type: str,
    context_type_quantity: str,
    context_type_value: str,
    date: str,
    description: str,
    input_profile: str,
    instance: str,
    jurisdiction: str,
    kind: str,
    name: str,
    output_profile: str,
    publisher: str,
    status: str,
    system: str,
    title: str,
    type_: str,
    url: str,
    version: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            base=base,
            code=code,
            context=context,
            context_quantity=context_quantity,
            context_type=context_type,
            context_type_quantity=context_type_quantity,
            context_type_value=context_type_value,
            date=date,
            description=description,
            input_profile=input_profile,
            instance=instance,
            jurisdiction=jurisdiction,
            kind=kind,
            name=name,
            output_profile=output_profile,
            publisher=publisher,
            status=status,
            system=system,
            title=title,
            type_=type_,
            url=url,
            version=version,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def organization_search(
    request: Request,
    response: Response,
    active: str,
    address: str,
    address_city: str,
    address_country: str,
    address_postalcode: str,
    address_state: str,
    address_use: str,
    endpoint: str,
    identifier: str,
    name: str,
    partof: str,
    phonetic: str,
    type_: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            active=active,
            address=address,
            address_city=address_city,
            address_country=address_country,
            address_postalcode=address_postalcode,
            address_state=address_state,
            address_use=address_use,
            endpoint=endpoint,
            identifier=identifier,
            name=name,
            partof=partof,
            phonetic=phonetic,
            type_=type_,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def organizationaffiliation_search(
    request: Request,
    response: Response,
    active: str,
    date: str,
    email: str,
    endpoint: str,
    identifier: str,
    location: str,
    network: str,
    participating_organization: str,
    phone: str,
    primary_organization: str,
    role: str,
    service: str,
    specialty: str,
    telecom: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            active=active,
            date=date,
            email=email,
            endpoint=endpoint,
            identifier=identifier,
            location=location,
            network=network,
            participating_organization=participating_organization,
            phone=phone,
            primary_organization=primary_organization,
            role=role,
            service=service,
            specialty=specialty,
            telecom=telecom,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def patient_search(
    request: Request,
    response: Response,
    active: str,
    address: str,
    address_city: str,
    address_country: str,
    address_postalcode: str,
    address_state: str,
    address_use: str,
    birthdate: str,
    death_date: str,
    deceased: str,
    email: str,
    family: str,
    gender: str,
    general_practitioner: str,
    given: str,
    identifier: str,
    language: str,
    link: str,
    name: str,
    organization: str,
    phone: str,
    phonetic: str,
    telecom: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            active=active,
            address=address,
            address_city=address_city,
            address_country=address_country,
            address_postalcode=address_postalcode,
            address_state=address_state,
            address_use=address_use,
            birthdate=birthdate,
            death_date=death_date,
            deceased=deceased,
            email=email,
            family=family,
            gender=gender,
            general_practitioner=general_practitioner,
            given=given,
            identifier=identifier,
            language=language,
            link=link,
            name=name,
            organization=organization,
            phone=phone,
            phonetic=phonetic,
            telecom=telecom,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def paymentnotice_search(
    request: Request,
    response: Response,
    created: str,
    identifier: str,
    payment_status: str,
    provider: str,
    request_: str,
    response_: str,
    status: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            created=created,
            identifier=identifier,
            payment_status=payment_status,
            provider=provider,
            request_=request_,
            response_=response_,
            status=status,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def paymentreconciliation_search(
    request: Request,
    response: Response,
    created: str,
    disposition: str,
    identifier: str,
    outcome: str,
    payment_issuer: str,
    request_: str,
    requestor: str,
    status: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            created=created,
            disposition=disposition,
            identifier=identifier,
            outcome=outcome,
            payment_issuer=payment_issuer,
            request_=request_,
            requestor=requestor,
            status=status,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def person_search(
    request: Request,
    response: Response,
    address: str,
    address_city: str,
    address_country: str,
    address_postalcode: str,
    address_state: str,
    address_use: str,
    birthdate: str,
    email: str,
    gender: str,
    identifier: str,
    link: str,
    name: str,
    organization: str,
    patient: str,
    phone: str,
    phonetic: str,
    practitioner: str,
    relatedperson: str,
    telecom: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            address=address,
            address_city=address_city,
            address_country=address_country,
            address_postalcode=address_postalcode,
            address_state=address_state,
            address_use=address_use,
            birthdate=birthdate,
            email=email,
            gender=gender,
            identifier=identifier,
            link=link,
            name=name,
            organization=organization,
            patient=patient,
            phone=phone,
            phonetic=phonetic,
            practitioner=practitioner,
            relatedperson=relatedperson,
            telecom=telecom,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def plandefinition_search(
    request: Request,
    response: Response,
    composed_of: str,
    context: str,
    context_quantity: str,
    context_type: str,
    context_type_quantity: str,
    context_type_value: str,
    date: str,
    definition: str,
    depends_on: str,
    derived_from: str,
    description: str,
    effective: str,
    identifier: str,
    jurisdiction: str,
    name: str,
    predecessor: str,
    publisher: str,
    status: str,
    successor: str,
    title: str,
    topic: str,
    type_: str,
    url: str,
    version: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            composed_of=composed_of,
            context=context,
            context_quantity=context_quantity,
            context_type=context_type,
            context_type_quantity=context_type_quantity,
            context_type_value=context_type_value,
            date=date,
            definition=definition,
            depends_on=depends_on,
            derived_from=derived_from,
            description=description,
            effective=effective,
            identifier=identifier,
            jurisdiction=jurisdiction,
            name=name,
            predecessor=predecessor,
            publisher=publisher,
            status=status,
            successor=successor,
            title=title,
            topic=topic,
            type_=type_,
            url=url,
            version=version,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def practitioner_search(
    request: Request,
    response: Response,
    active: str,
    address: str,
    address_city: str,
    address_country: str,
    address_postalcode: str,
    address_state: str,
    address_use: str,
    communication: str,
    email: str,
    family: str,
    gender: str,
    given: str,
    identifier: str,
    name: str,
    phone: str,
    phonetic: str,
    telecom: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            active=active,
            address=address,
            address_city=address_city,
            address_country=address_country,
            address_postalcode=address_postalcode,
            address_state=address_state,
            address_use=address_use,
            communication=communication,
            email=email,
            family=family,
            gender=gender,
            given=given,
            identifier=identifier,
            name=name,
            phone=phone,
            phonetic=phonetic,
            telecom=telecom,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def practitionerrole_search(
    request: Request,
    response: Response,
    active: str,
    date: str,
    email: str,
    endpoint: str,
    identifier: str,
    location: str,
    organization: str,
    phone: str,
    practitioner: str,
    role: str,
    service: str,
    specialty: str,
    telecom: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            active=active,
            date=date,
            email=email,
            endpoint=endpoint,
            identifier=identifier,
            location=location,
            organization=organization,
            phone=phone,
            practitioner=practitioner,
            role=role,
            service=service,
            specialty=specialty,
            telecom=telecom,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def procedure_search(
    request: Request,
    response: Response,
    based_on: str,
    category: str,
    code: str,
    date: str,
    encounter: str,
    identifier: str,
    instantiates_canonical: str,
    instantiates_uri: str,
    location: str,
    part_of: str,
    patient: str,
    performer: str,
    reason_code: str,
    reason_reference: str,
    status: str,
    subject: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            based_on=based_on,
            category=category,
            code=code,
            date=date,
            encounter=encounter,
            identifier=identifier,
            instantiates_canonical=instantiates_canonical,
            instantiates_uri=instantiates_uri,
            location=location,
            part_of=part_of,
            patient=patient,
            performer=performer,
            reason_code=reason_code,
            reason_reference=reason_reference,
            status=status,
            subject=subject,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def provenance_search(
    request: Request,
    response: Response,
    agent: str,
    agent_role: str,
    agent_type: str,
    entity: str,
    location: str,
    patient: str,
    recorded: str,
    signature_type: str,
    target: str,
    when: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            agent=agent,
            agent_role=agent_role,
            agent_type=agent_type,
            entity=entity,
            location=location,
            patient=patient,
            recorded=recorded,
            signature_type=signature_type,
            target=target,
            when=when,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def questionnaire_search(
    request: Request,
    response: Response,
    code: str,
    context: str,
    context_quantity: str,
    context_type: str,
    context_type_quantity: str,
    context_type_value: str,
    date: str,
    definition: str,
    description: str,
    effective: str,
    identifier: str,
    jurisdiction: str,
    name: str,
    publisher: str,
    status: str,
    subject_type: str,
    title: str,
    url: str,
    version: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            code=code,
            context=context,
            context_quantity=context_quantity,
            context_type=context_type,
            context_type_quantity=context_type_quantity,
            context_type_value=context_type_value,
            date=date,
            definition=definition,
            description=description,
            effective=effective,
            identifier=identifier,
            jurisdiction=jurisdiction,
            name=name,
            publisher=publisher,
            status=status,
            subject_type=subject_type,
            title=title,
            url=url,
            version=version,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def questionnaireresponse_search(
    request: Request,
    response: Response,
    author: str,
    authored: str,
    based_on: str,
    encounter: str,
    identifier: str,
    part_of: str,
    patient: str,
    questionnaire: str,
    source: str,
    status: str,
    subject: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            author=author,
            authored=authored,
            based_on=based_on,
            encounter=encounter,
            identifier=identifier,
            part_of=part_of,
            patient=patient,
            questionnaire=questionnaire,
            source=source,
            status=status,
            subject=subject,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def relatedperson_search(
    request: Request,
    response: Response,
    active: str,
    address: str,
    address_city: str,
    address_country: str,
    address_postalcode: str,
    address_state: str,
    address_use: str,
    birthdate: str,
    email: str,
    gender: str,
    identifier: str,
    name: str,
    patient: str,
    phone: str,
    phonetic: str,
    relationship: str,
    telecom: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            active=active,
            address=address,
            address_city=address_city,
            address_country=address_country,
            address_postalcode=address_postalcode,
            address_state=address_state,
            address_use=address_use,
            birthdate=birthdate,
            email=email,
            gender=gender,
            identifier=identifier,
            name=name,
            patient=patient,
            phone=phone,
            phonetic=phonetic,
            relationship=relationship,
            telecom=telecom,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def requestgroup_search(
    request: Request,
    response: Response,
    author: str,
    authored: str,
    code: str,
    encounter: str,
    group_identifier: str,
    identifier: str,
    instantiates_canonical: str,
    instantiates_uri: str,
    intent: str,
    participant: str,
    patient: str,
    priority: str,
    status: str,
    subject: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            author=author,
            authored=authored,
            code=code,
            encounter=encounter,
            group_identifier=group_identifier,
            identifier=identifier,
            instantiates_canonical=instantiates_canonical,
            instantiates_uri=instantiates_uri,
            intent=intent,
            participant=participant,
            patient=patient,
            priority=priority,
            status=status,
            subject=subject,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def researchdefinition_search(
    request: Request,
    response: Response,
    composed_of: str,
    context: str,
    context_quantity: str,
    context_type: str,
    context_type_quantity: str,
    context_type_value: str,
    date: str,
    depends_on: str,
    derived_from: str,
    description: str,
    effective: str,
    identifier: str,
    jurisdiction: str,
    name: str,
    predecessor: str,
    publisher: str,
    status: str,
    successor: str,
    title: str,
    topic: str,
    url: str,
    version: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            composed_of=composed_of,
            context=context,
            context_quantity=context_quantity,
            context_type=context_type,
            context_type_quantity=context_type_quantity,
            context_type_value=context_type_value,
            date=date,
            depends_on=depends_on,
            derived_from=derived_from,
            description=description,
            effective=effective,
            identifier=identifier,
            jurisdiction=jurisdiction,
            name=name,
            predecessor=predecessor,
            publisher=publisher,
            status=status,
            successor=successor,
            title=title,
            topic=topic,
            url=url,
            version=version,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def researchelementdefinition_search(
    request: Request,
    response: Response,
    composed_of: str,
    context: str,
    context_quantity: str,
    context_type: str,
    context_type_quantity: str,
    context_type_value: str,
    date: str,
    depends_on: str,
    derived_from: str,
    description: str,
    effective: str,
    identifier: str,
    jurisdiction: str,
    name: str,
    predecessor: str,
    publisher: str,
    status: str,
    successor: str,
    title: str,
    topic: str,
    url: str,
    version: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            composed_of=composed_of,
            context=context,
            context_quantity=context_quantity,
            context_type=context_type,
            context_type_quantity=context_type_quantity,
            context_type_value=context_type_value,
            date=date,
            depends_on=depends_on,
            derived_from=derived_from,
            description=description,
            effective=effective,
            identifier=identifier,
            jurisdiction=jurisdiction,
            name=name,
            predecessor=predecessor,
            publisher=publisher,
            status=status,
            successor=successor,
            title=title,
            topic=topic,
            url=url,
            version=version,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def researchstudy_search(
    request: Request,
    response: Response,
    category: str,
    date: str,
    focus: str,
    identifier: str,
    keyword: str,
    location: str,
    partof: str,
    principalinvestigator: str,
    protocol: str,
    site: str,
    sponsor: str,
    status: str,
    title: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            category=category,
            date=date,
            focus=focus,
            identifier=identifier,
            keyword=keyword,
            location=location,
            partof=partof,
            principalinvestigator=principalinvestigator,
            protocol=protocol,
            site=site,
            sponsor=sponsor,
            status=status,
            title=title,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def researchsubject_search(
    request: Request,
    response: Response,
    date: str,
    identifier: str,
    individual: str,
    patient: str,
    status: str,
    study: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            date=date,
            identifier=identifier,
            individual=individual,
            patient=patient,
            status=status,
            study=study,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def riskassessment_search(
    request: Request,
    response: Response,
    condition: str,
    date: str,
    encounter: str,
    identifier: str,
    method: str,
    patient: str,
    performer: str,
    probability: str,
    risk: str,
    subject: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            condition=condition,
            date=date,
            encounter=encounter,
            identifier=identifier,
            method=method,
            patient=patient,
            performer=performer,
            probability=probability,
            risk=risk,
            subject=subject,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def riskevidencesynthesis_search(
    request: Request,
    response: Response,
    context: str,
    context_quantity: str,
    context_type: str,
    context_type_quantity: str,
    context_type_value: str,
    date: str,
    description: str,
    effective: str,
    identifier: str,
    jurisdiction: str,
    name: str,
    publisher: str,
    status: str,
    title: str,
    url: str,
    version: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            context=context,
            context_quantity=context_quantity,
            context_type=context_type,
            context_type_quantity=context_type_quantity,
            context_type_value=context_type_value,
            date=date,
            description=description,
            effective=effective,
            identifier=identifier,
            jurisdiction=jurisdiction,
            name=name,
            publisher=publisher,
            status=status,
            title=title,
            url=url,
            version=version,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def schedule_search(
    request: Request,
    response: Response,
    active: str,
    actor: str,
    date: str,
    identifier: str,
    service_category: str,
    service_type: str,
    specialty: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            active=active,
            actor=actor,
            date=date,
            identifier=identifier,
            service_category=service_category,
            service_type=service_type,
            specialty=specialty,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def searchparameter_search(
    request: Request,
    response: Response,
    base: str,
    code: str,
    component: str,
    context: str,
    context_quantity: str,
    context_type: str,
    context_type_quantity: str,
    context_type_value: str,
    date: str,
    derived_from: str,
    description: str,
    jurisdiction: str,
    name: str,
    publisher: str,
    status: str,
    target: str,
    type_: str,
    url: str,
    version: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            base=base,
            code=code,
            component=component,
            context=context,
            context_quantity=context_quantity,
            context_type=context_type,
            context_type_quantity=context_type_quantity,
            context_type_value=context_type_value,
            date=date,
            derived_from=derived_from,
            description=description,
            jurisdiction=jurisdiction,
            name=name,
            publisher=publisher,
            status=status,
            target=target,
            type_=type_,
            url=url,
            version=version,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def servicerequest_search(
    request: Request,
    response: Response,
    authored: str,
    based_on: str,
    body_site: str,
    category: str,
    code: str,
    encounter: str,
    identifier: str,
    instantiates_canonical: str,
    instantiates_uri: str,
    intent: str,
    occurrence: str,
    patient: str,
    performer: str,
    performer_type: str,
    priority: str,
    replaces: str,
    requester: str,
    requisition: str,
    specimen: str,
    status: str,
    subject: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            authored=authored,
            based_on=based_on,
            body_site=body_site,
            category=category,
            code=code,
            encounter=encounter,
            identifier=identifier,
            instantiates_canonical=instantiates_canonical,
            instantiates_uri=instantiates_uri,
            intent=intent,
            occurrence=occurrence,
            patient=patient,
            performer=performer,
            performer_type=performer_type,
            priority=priority,
            replaces=replaces,
            requester=requester,
            requisition=requisition,
            specimen=specimen,
            status=status,
            subject=subject,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def slot_search(
    request: Request,
    response: Response,
    appointment_type: str,
    identifier: str,
    schedule: str,
    service_category: str,
    service_type: str,
    specialty: str,
    start: str,
    status: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            appointment_type=appointment_type,
            identifier=identifier,
            schedule=schedule,
            service_category=service_category,
            service_type=service_type,
            specialty=specialty,
            start=start,
            status=status,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def specimen_search(
    request: Request,
    response: Response,
    accession: str,
    bodysite: str,
    collected: str,
    collector: str,
    container: str,
    container_id: str,
    identifier: str,
    parent: str,
    patient: str,
    status: str,
    subject: str,
    type_: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            accession=accession,
            bodysite=bodysite,
            collected=collected,
            collector=collector,
            container=container,
            container_id=container_id,
            identifier=identifier,
            parent=parent,
            patient=patient,
            status=status,
            subject=subject,
            type_=type_,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def specimendefinition_search(
    request: Request, response: Response, container: str, identifier: str, type_: str
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(container=container, identifier=identifier, type_=type_),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def structuredefinition_search(
    request: Request,
    response: Response,
    abstract: str,
    base: str,
    base_path: str,
    context: str,
    context_quantity: str,
    context_type: str,
    context_type_quantity: str,
    context_type_value: str,
    date: str,
    derivation: str,
    description: str,
    experimental: str,
    ext_context: str,
    identifier: str,
    jurisdiction: str,
    keyword: str,
    kind: str,
    name: str,
    path: str,
    publisher: str,
    status: str,
    title: str,
    type_: str,
    url: str,
    valueset: str,
    version: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            abstract=abstract,
            base=base,
            base_path=base_path,
            context=context,
            context_quantity=context_quantity,
            context_type=context_type,
            context_type_quantity=context_type_quantity,
            context_type_value=context_type_value,
            date=date,
            derivation=derivation,
            description=description,
            experimental=experimental,
            ext_context=ext_context,
            identifier=identifier,
            jurisdiction=jurisdiction,
            keyword=keyword,
            kind=kind,
            name=name,
            path=path,
            publisher=publisher,
            status=status,
            title=title,
            type_=type_,
            url=url,
            valueset=valueset,
            version=version,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def structuremap_search(
    request: Request,
    response: Response,
    context: str,
    context_quantity: str,
    context_type: str,
    context_type_quantity: str,
    context_type_value: str,
    date: str,
    description: str,
    identifier: str,
    jurisdiction: str,
    name: str,
    publisher: str,
    status: str,
    title: str,
    url: str,
    version: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            context=context,
            context_quantity=context_quantity,
            context_type=context_type,
            context_type_quantity=context_type_quantity,
            context_type_value=context_type_value,
            date=date,
            description=description,
            identifier=identifier,
            jurisdiction=jurisdiction,
            name=name,
            publisher=publisher,
            status=status,
            title=title,
            url=url,
            version=version,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def subscription_search(
    request: Request,
    response: Response,
    contact: str,
    criteria: str,
    payload: str,
    status: str,
    type_: str,
    url: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            contact=contact,
            criteria=criteria,
            payload=payload,
            status=status,
            type_=type_,
            url=url,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def substance_search(
    request: Request,
    response: Response,
    category: str,
    code: str,
    container_identifier: str,
    expiry: str,
    identifier: str,
    quantity: str,
    status: str,
    substance_reference: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            category=category,
            code=code,
            container_identifier=container_identifier,
            expiry=expiry,
            identifier=identifier,
            quantity=quantity,
            status=status,
            substance_reference=substance_reference,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def substancespecification_search(
    request: Request, response: Response, code: str
) -> FHIRResourceType:
    result = cast(FHIRInteractionResult[FHIRResourceType], await callable_(code=code))
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def supplydelivery_search(
    request: Request,
    response: Response,
    identifier: str,
    patient: str,
    receiver: str,
    status: str,
    supplier: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            identifier=identifier,
            patient=patient,
            receiver=receiver,
            status=status,
            supplier=supplier,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def supplyrequest_search(
    request: Request,
    response: Response,
    category: str,
    date: str,
    identifier: str,
    requester: str,
    status: str,
    subject: str,
    supplier: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            category=category,
            date=date,
            identifier=identifier,
            requester=requester,
            status=status,
            subject=subject,
            supplier=supplier,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def task_search(
    request: Request,
    response: Response,
    authored_on: str,
    based_on: str,
    business_status: str,
    code: str,
    encounter: str,
    focus: str,
    group_identifier: str,
    identifier: str,
    intent: str,
    modified: str,
    owner: str,
    part_of: str,
    patient: str,
    performer: str,
    period: str,
    priority: str,
    requester: str,
    status: str,
    subject: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            authored_on=authored_on,
            based_on=based_on,
            business_status=business_status,
            code=code,
            encounter=encounter,
            focus=focus,
            group_identifier=group_identifier,
            identifier=identifier,
            intent=intent,
            modified=modified,
            owner=owner,
            part_of=part_of,
            patient=patient,
            performer=performer,
            period=period,
            priority=priority,
            requester=requester,
            status=status,
            subject=subject,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def terminologycapabilities_search(
    request: Request,
    response: Response,
    context: str,
    context_quantity: str,
    context_type: str,
    context_type_quantity: str,
    context_type_value: str,
    date: str,
    description: str,
    jurisdiction: str,
    name: str,
    publisher: str,
    status: str,
    title: str,
    url: str,
    version: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            context=context,
            context_quantity=context_quantity,
            context_type=context_type,
            context_type_quantity=context_type_quantity,
            context_type_value=context_type_value,
            date=date,
            description=description,
            jurisdiction=jurisdiction,
            name=name,
            publisher=publisher,
            status=status,
            title=title,
            url=url,
            version=version,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def testreport_search(
    request: Request,
    response: Response,
    identifier: str,
    issued: str,
    participant: str,
    result_: str,
    tester: str,
    testscript: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            identifier=identifier,
            issued=issued,
            participant=participant,
            result_=result_,
            tester=tester,
            testscript=testscript,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def testscript_search(
    request: Request,
    response: Response,
    context: str,
    context_quantity: str,
    context_type: str,
    context_type_quantity: str,
    context_type_value: str,
    date: str,
    description: str,
    identifier: str,
    jurisdiction: str,
    name: str,
    publisher: str,
    status: str,
    testscript_capability: str,
    title: str,
    url: str,
    version: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            context=context,
            context_quantity=context_quantity,
            context_type=context_type,
            context_type_quantity=context_type_quantity,
            context_type_value=context_type_value,
            date=date,
            description=description,
            identifier=identifier,
            jurisdiction=jurisdiction,
            name=name,
            publisher=publisher,
            status=status,
            testscript_capability=testscript_capability,
            title=title,
            url=url,
            version=version,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def valueset_search(
    request: Request,
    response: Response,
    code: str,
    context: str,
    context_quantity: str,
    context_type: str,
    context_type_quantity: str,
    context_type_value: str,
    date: str,
    description: str,
    expansion: str,
    identifier: str,
    jurisdiction: str,
    name: str,
    publisher: str,
    reference: str,
    status: str,
    title: str,
    url: str,
    version: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            code=code,
            context=context,
            context_quantity=context_quantity,
            context_type=context_type,
            context_type_quantity=context_type_quantity,
            context_type_value=context_type_value,
            date=date,
            description=description,
            expansion=expansion,
            identifier=identifier,
            jurisdiction=jurisdiction,
            name=name,
            publisher=publisher,
            reference=reference,
            status=status,
            title=title,
            url=url,
            version=version,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def verificationresult_search(
    request: Request, response: Response, target: str
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType], await callable_(target=target)
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource


async def visionprescription_search(
    request: Request,
    response: Response,
    datewritten: str,
    encounter: str,
    identifier: str,
    patient: str,
    prescriber: str,
    status: str,
) -> FHIRResourceType:
    result = cast(
        FHIRInteractionResult[FHIRResourceType],
        await callable_(
            datewritten=datewritten,
            encounter=encounter,
            identifier=identifier,
            patient=patient,
            prescriber=prescriber,
            status=status,
        ),
    )
    result.validate()

    assert result.resource is not None, "FHIR search interaction must return a bundle"

    return result.resource
