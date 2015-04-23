import eu.liderproject.lixr._

new ModelWithMappings {
  val dc = Namespace("http://purl.org/dc/elements/1.1/")
  val dcat = Namespace("http://www.w3.org/ns/dcat#")
  val dct = Namespace("http://purl.org/dc/terms/")
  val elra = Namespace("http://www.openarchives.org/OAI/2.0/static-repository")
  val foaf = Namespace("http://xmlns.com/foaf/0.1/")
  val oai = Namespace("http://www.openarchives.org/OAI/2.0/")
  val olac = Namespace("http://www.language-archives.org/OLAC/1.1/")

  elra.Repository --> (
    handle(elra.Identify),
    handle(elra.ListMetadataFormats),
    handle(elra.ListRecords)
  )

  elra.Identify --> ()

  elra.ListMetadataFormats --> ()

  elra.ListRecords --> (
    handle(oai.record)
  )

  oai.record --> (
    set("identifier", content(oai.header \ oai.identifier).replace(".*:([^:]+)$","$1")) (
      node(get("identifier")) (
        a > dcat.Dataset,
        handle(oai.header),
        handle(oai.metadata)
      )
    )
  )

  oai.header --> (
    foaf.primaryTopic < node(get("identifier") :+ "#Header") (
      a > dcat.CatalogRecord,
      stringMap(oai.identifier, dc.identifier),
      dateMap(oai.datestamp, dct.issued)
    )
  )

  oai.metadata --> (
    handle(olac.olac)
  )

  olac.olac --> (
    stringMap(dc.title, dc.title),
    stringMap(dc.language, dc.language),
    forall(dc.`type`) (
      when(content.exists) (
        dc.`type` > content
      ) otherwise (
        dct.`type` > (olac + att(olac.code))
      )
    ),
    stringMap(dc.description, dc.description),
    stringMap(dct.`abstract`, dct.`abstract`),
    stringMap(dc.publisher, dc.publisher),
    forall(dc.identifier) (
      when(content.matches("^http:.*$")) (
        dcat.distribution > node(get("identifier") :+ "#Distribution") (
          a > dcat.Distribution, 
          dcat.accessURL > uri(content)
        )
      )
    ),
    stringMap(dc.coverage, dc.coverage),
    stringMap(dct.accessRights, dct.accessRights),
    dateMap(dct.available, dct.available),
    dateMap(dct.issued, dct.issued),
    dateMap(dct.modified, dct.modified),
    stringMap(dct.medium, dct.medium)
// Always empty
//    stringMap(dc.format, dc.format),
//    stringMap(dct.extent, dct.extent),
//    stringMap(dc.source, dc.source),
    
    
  )
}

