import eu.liderproject.lixr._

new ModelWithMappings {
  val dc = Namespace("http://purl.org/dc/elements/1.1/")
  val dcat = Namespace("http://www.w3.org/ns/dcat#")
  val dct = Namespace("http://purl.org/dc/terms/")
  val foaf = Namespace("http://xmlns.com/foaf/0.1/")
  val oai = Namespace("http://www.openarchives.org/OAI/2.0/")
  val olac = Namespace("http://www.language-archives.org/OLAC/1.0/")

  oai.`OAI-PMH` --> (
    handle(oai.ListRecords)
  )

  oai.ListRecords --> (
    handle(oai.record)
  )

  oai.record --> (
    set("identifier", content(oai.header \ oai.identifier).replace("\\s","").replace(":","__")) (
      node(get("identifier")) (
        handle(oai.header),
        handle(oai.metadata)
      )
    )
  )

  oai.header --> (
    foaf.primaryTopic < node(get("identifier") :+ "#Header") (
      a > dcat.CatalogRecord,
      dateMap(oai.datestamp, dct.issued)
    )
  )

  oai.metadata --> (
    stringMap(dc.title, dc.title),
    stringMap(dc.creator, dc.creator),
    stringMap(dc.subject, dc.subject),
    stringMap(dc.description, dc.description),
    stringMap(dc.publisher, dc.publisher),
    stringMap(dc.contributor, dc.contributor),
    dateMap(dc.date, dc.date),
    stringMap(dc.`type`, dc.`type`),
    stringMap(dc.format, dc.format),
    forall(dc.identifier) (
      dcat.distribution > node(frag(get("identifier") :+ "#Distribution")) (
        a > dcat.Distribution,
        dcat.accessURL > uri(content)
      )
    ),
    stringMap(dc.source, dc.source),
    stringMap(dc.language, dc.language),
    stringMap(dc.relation, dc.relation),
    stringMap(dc.coverage, dc.coverage),
    stringMap(dc.rights, dc.rights)
  )
}

