<!DOCTYPE xsl:stylesheet>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:cmd="http://www.clarin.eu/cmd/" xmlns:cmdi="http://www.clarin.eu/cmd/" xmlns:dcat="http://www.w3.org/ns/dcat#" xmlns:foaf="http://xmlns.com/foaf/0.1/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dct="http://purl.org/dc/terms/">
  <xsl:strip-space elements="*"></xsl:strip-space>
  <xsl:output method="xml" indent="yes"></xsl:output>
  <xsl:template match="/cmd:CMD">
    <rdf:RDF>
      <dcat:CatalogRecord rdf:about="#Header">
        <xsl:apply-templates select="cmd:Header"></xsl:apply-templates>
        <foaf:primaryTopic>
          <dcat:Dataset rdf:about="">
            <xsl:apply-templates select="cmd:Resources"></xsl:apply-templates>
            <xsl:apply-templates select="cmd:Components"></xsl:apply-templates>
          </dcat:Dataset>
        </foaf:primaryTopic>
      </dcat:CatalogRecord>
    </rdf:RDF>
  </xsl:template>
  <xsl:template match="cmd:Header">
    <xsl:apply-templates select="cmd:MdCreator"></xsl:apply-templates>
    <xsl:apply-templates select="cmd:MdCreationDate"></xsl:apply-templates>
    <xsl:apply-templates select="cmd:MdSelfLink"></xsl:apply-templates>
    <xsl:apply-templates select="cmd:MdProfile"></xsl:apply-templates>
    <xsl:apply-templates select="cmd:MdCollectionDisplayName"></xsl:apply-templates>
  </xsl:template>
  <xsl:template match="cmd:MdCreator">
    <dc:creator>
      <xsl:value-of select="."></xsl:value-of>
    </dc:creator>
  </xsl:template>
  <xsl:template match="cmd:MdCreationDate">
    <xsl:if test="text()!=''">
      <dct:issued rdf:datatype="http://www.w3.org/2001/XMLSchema#date">
        <xsl:value-of select="."></xsl:value-of>
      </dct:issued>
    </xsl:if>
  </xsl:template>
  <xsl:template match="cmd:MdSelfLink">
    <cmd:MdSelfLink>
      <xsl:value-of select="."></xsl:value-of>
    </cmd:MdSelfLink>
  </xsl:template>
  <xsl:template match="cmd:MdProfile">
    <cmd:MdProfile>
      <xsl:value-of select="."></xsl:value-of>
    </cmd:MdProfile>
  </xsl:template>
  <xsl:template match="cmd:MdCollectionDisplayName">
    <dc:title>
      <xsl:value-of select="."></xsl:value-of>
    </dc:title>
  </xsl:template>
  <xsl:template match="cmd:Resources">
    <xsl:apply-templates select="cmd:ResourceProxyList"></xsl:apply-templates>
    <xsl:apply-templates select="cmd:JournalFileProxyList"></xsl:apply-templates>
    <xsl:apply-templates select="cmd:ResourceRelationList"></xsl:apply-templates>
    <xsl:apply-templates select="cmd:IsPartOfList"></xsl:apply-templates>
  </xsl:template>
  <xsl:template match="cmd:ResourceProxyList">
    <xsl:apply-templates select="cmd:ResourceProxy"></xsl:apply-templates>
  </xsl:template>
  <xsl:template match="cmd:ResourceProxy">
    <dcat:distribution>
      <dcat:Distribution>
        <xsl:attribute name="rdf:about">
          <xsl:value-of select="concat('#',@id)"></xsl:value-of>
        </xsl:attribute>
        <xsl:apply-templates select="cmd:ResourceType"></xsl:apply-templates>
        <xsl:apply-templates select="cmd:ResourceRef"></xsl:apply-templates>
      </dcat:Distribution>
    </dcat:distribution>
  </xsl:template>
  <xsl:template match="cmd:ResourceType">
    <cmd:ResourceType>
      <xsl:value-of select="."></xsl:value-of>
    </cmd:ResourceType>
  </xsl:template>
  <xsl:template match="cmd:ResourceRef">
    <dcat:accessURL>
      <xsl:call-template name="uri">
        <xsl:with-param name="u" select="."></xsl:with-param>
      </xsl:call-template>
    </dcat:accessURL>
  </xsl:template>
  <xsl:template match="cmd:JournalFileProxyList">
    <xsl:if test="*">
      <xsl:message>
        <xsl:value-of select="concat('JournalFileProxyList',.)"></xsl:value-of>
      </xsl:message>
    </xsl:if>
  </xsl:template>
  <xsl:template match="cmd:ResourceRelationList">
    <xsl:if test="*">
      <xsl:message>
        <xsl:value-of select="concat('ResourceRelationList',.)"></xsl:value-of>
      </xsl:message>
    </xsl:if>
  </xsl:template>
  <xsl:template match="cmd:IsPartOfList">
    <xsl:apply-templates select="cmd:IsPartOf"></xsl:apply-templates>
  </xsl:template>
  <xsl:template match="cmd:IsPartOf">
    <cmd:IsPartOf>
      <xsl:call-template name="uri">
        <xsl:with-param name="u" select="."></xsl:with-param>
      </xsl:call-template>
    </cmd:IsPartOf>
  </xsl:template>
  <xsl:template match="cmd:Components">
    <xsl:apply-templates select="cmd:OLAC-DcmiTerms"></xsl:apply-templates>
    <xsl:apply-templates select="cmd:DcmiTerms"></xsl:apply-templates>
  </xsl:template>
  <xsl:template match="cmd:OLAC-DcmiTerms|cmd:DcmiTerms">
    <xsl:if test="cmd:abstract!=''">
      <dct:abstract>
        <xsl:value-of select="cmd:abstract"></xsl:value-of>
      </dct:abstract>
    </xsl:if>
    <xsl:if test="cmd:accessRights!=''">
      <dct:accessRights>
        <xsl:value-of select="cmd:accessRights"></xsl:value-of>
      </dct:accessRights>
    </xsl:if>
    <xsl:if test="cmd:accrualMethod!=''">
      <dct:accrualMethod>
        <xsl:value-of select="cmd:accrualMethod"></xsl:value-of>
      </dct:accrualMethod>
    </xsl:if>
    <xsl:if test="cmd:accrualPeriodicity!=''">
      <dct:accrualPeriodicity>
        <xsl:value-of select="cmd:accrualPeriodicity"></xsl:value-of>
      </dct:accrualPeriodicity>
    </xsl:if>
    <xsl:if test="cmd:accrualPolicy!=''">
      <dct:accrualPolicy>
        <xsl:value-of select="cmd:accrualPolicy"></xsl:value-of>
      </dct:accrualPolicy>
    </xsl:if>
    <xsl:if test="cmd:alternative!=''">
      <dct:alternative>
        <xsl:value-of select="cmd:alternative"></xsl:value-of>
      </dct:alternative>
    </xsl:if>
    <xsl:if test="cmd:audience!=''">
      <dct:audience>
        <xsl:value-of select="cmd:audience"></xsl:value-of>
      </dct:audience>
    </xsl:if>
    <xsl:if test="cmd:available!=''">
      <dct:available>
        <xsl:value-of select="cmd:available"></xsl:value-of>
      </dct:available>
    </xsl:if>
    <xsl:if test="cmd:bibliographicCitation!=''">
      <dct:bibliographicCitation>
        <xsl:value-of select="cmd:bibliographicCitation"></xsl:value-of>
      </dct:bibliographicCitation>
    </xsl:if>
    <xsl:if test="cmd:conformsTo!=''">
      <dct:conformsTo>
        <xsl:value-of select="cmd:conformsTo"></xsl:value-of>
      </dct:conformsTo>
    </xsl:if>
    <xsl:if test="cmd:contributor!=''">
      <dc:contributor>
        <xsl:value-of select="cmd:contributor"></xsl:value-of>
      </dc:contributor>
    </xsl:if>
    <xsl:if test="cmd:coverage!=''">
      <dc:coverage>
        <xsl:value-of select="cmd:coverage"></xsl:value-of>
      </dc:coverage>
    </xsl:if>
    <xsl:if test="cmd:!='created'">
      <dct:created>
        <xsl:value-of select="cmd:created"></xsl:value-of>
      </dct:created>
    </xsl:if>
    <xsl:if test="cmd:creator!=''">
      <dc:creator>
        <xsl:value-of select="cmd:creator"></xsl:value-of>
      </dc:creator>
    </xsl:if>
    <xsl:if test="cmd:date!=''">
      <dc:date>
        <xsl:value-of select="cmd:date"></xsl:value-of>
      </dc:date>
    </xsl:if>
    <xsl:if test="cmd:dateAccepted!=''">
      <dct:dateAccepted>
        <xsl:value-of select="cmd:dateAccepted"></xsl:value-of>
      </dct:dateAccepted>
    </xsl:if>
    <xsl:if test="cmd:dateSubmitted!=''">
      <dct:dateSubmitted>
        <xsl:value-of select="cmd:dateSubmitted"></xsl:value-of>
      </dct:dateSubmitted>
    </xsl:if>
    <xsl:if test="cmd:description!=''">
      <dc:description>
        <xsl:value-of select="cmd:description"></xsl:value-of>
      </dc:description>
    </xsl:if>
    <xsl:if test="cmd:educationLevel!=''">
      <dct:educationLevel>
        <xsl:value-of select="cmd:educationLevel"></xsl:value-of>
      </dct:educationLevel>
    </xsl:if>
    <xsl:if test="cmd:extent!=''">
      <dct:extent>
        <xsl:value-of select="cmd:extent"></xsl:value-of>
      </dct:extent>
    </xsl:if>
    <xsl:if test="cmd:format!=''">
      <dc:format>
        <xsl:value-of select="cmd:format"></xsl:value-of>
      </dc:format>
    </xsl:if>
    <xsl:if test="cmd:hasFormat!=''">
      <dct:hasFormat>
        <xsl:value-of select="cmd:hasFormat"></xsl:value-of>
      </dct:hasFormat>
    </xsl:if>
    <xsl:if test="cmd:hasPart!=''">
      <dct:hasPart>
        <xsl:value-of select="cmd:hasPart"></xsl:value-of>
      </dct:hasPart>
    </xsl:if>
    <xsl:if test="cmd:hasVersion!=''">
      <dct:hasVersion>
        <xsl:value-of select="cmd:hasVersion"></xsl:value-of>
      </dct:hasVersion>
    </xsl:if>
    <xsl:if test="cmd:relation!=''">
      <dc:relation>
        <xsl:value-of select="cmd:relation"></xsl:value-of>
      </dc:relation>
    </xsl:if>
    <xsl:if test="cmd:identifier!=''">
      <dc:identifier>
        <xsl:value-of select="cmd:identifier"></xsl:value-of>
      </dc:identifier>
    </xsl:if>
    <xsl:if test="cmd:instructionalMethod!=''">
      <dct:instructionalMethod>
        <xsl:value-of select="cmd:instructionalMethod"></xsl:value-of>
      </dct:instructionalMethod>
    </xsl:if>
    <xsl:if test="cmd:isFormatOf!=''">
      <dct:isFormatOf>
        <xsl:value-of select="cmd:isFormatOf"></xsl:value-of>
      </dct:isFormatOf>
    </xsl:if>
    <xsl:if test="cmd:isPartOf!=''">
      <dct:isPartOf>
        <xsl:value-of select="cmd:isPartOf"></xsl:value-of>
      </dct:isPartOf>
    </xsl:if>
    <xsl:if test="cmd:isReferencedBy!=''">
      <dct:isReferencedBy>
        <xsl:value-of select="cmd:isReferencedBy"></xsl:value-of>
      </dct:isReferencedBy>
    </xsl:if>
    <xsl:if test="cmd:isReplacedBy!=''">
      <dct:isReplacedBy>
        <xsl:value-of select="cmd:isReplacedBy"></xsl:value-of>
      </dct:isReplacedBy>
    </xsl:if>
    <xsl:if test="cmd:isRequiredBy!=''">
      <dct:isRequiredBy>
        <xsl:value-of select="cmd:isRequiredBy"></xsl:value-of>
      </dct:isRequiredBy>
    </xsl:if>
    <xsl:if test="cmd:issued!=''">
      <dct:issued>
        <xsl:value-of select="cmd:issued"></xsl:value-of>
      </dct:issued>
    </xsl:if>
    <xsl:if test="cmd:isVersionOf!=''">
      <dct:isVersionOf>
        <xsl:value-of select="cmd:isVersionOf"></xsl:value-of>
      </dct:isVersionOf>
    </xsl:if>
    <xsl:if test="cmd:language!=''">
      <dc:language>
        <xsl:value-of select="cmd:language"></xsl:value-of>
      </dc:language>
    </xsl:if>
    <xsl:if test="cmd:license!=''">
      <dct:license>
        <xsl:value-of select="cmd:license"></xsl:value-of>
      </dct:license>
    </xsl:if>
    <xsl:if test="cmd:mediator!=''">
      <dct:mediator>
        <xsl:value-of select="cmd:mediator"></xsl:value-of>
      </dct:mediator>
    </xsl:if>
    <xsl:if test="cmd:medium!=''">
      <dct:medium>
        <xsl:value-of select="cmd:medium"></xsl:value-of>
      </dct:medium>
    </xsl:if>
    <xsl:if test="cmd:modified!=''">
      <dct:modified>
        <xsl:value-of select="cmd:modified"></xsl:value-of>
      </dct:modified>
    </xsl:if>
    <xsl:if test="cmd:provenance!=''">
      <dct:provenance>
        <xsl:value-of select="cmd:provenance"></xsl:value-of>
      </dct:provenance>
    </xsl:if>
    <xsl:if test="cmd:publisher!=''">
      <dc:publisher>
        <xsl:value-of select="cmd:publisher"></xsl:value-of>
      </dc:publisher>
    </xsl:if>
    <xsl:if test="cmd:references!=''">
      <dct:references>
        <xsl:value-of select="cmd:references"></xsl:value-of>
      </dct:references>
    </xsl:if>
    <xsl:if test="cmd:relation!=''">
      <dct:relation>
        <xsl:value-of select="cmd:relation"></xsl:value-of>
      </dct:relation>
    </xsl:if>
    <xsl:if test="cmd:replaces!=''">
      <dct:replaces>
        <xsl:value-of select="cmd:replaces"></xsl:value-of>
      </dct:replaces>
    </xsl:if>
    <xsl:if test="cmd:requires!=''">
      <dct:requires>
        <xsl:value-of select="cmd:requires"></xsl:value-of>
      </dct:requires>
    </xsl:if>
    <xsl:if test="cmd:rights!=''">
      <dc:rights>
        <xsl:value-of select="cmd:rights"></xsl:value-of>
      </dc:rights>
    </xsl:if>
    <xsl:if test="cmd:rightsHolder!=''">
      <dct:rightsHolder>
        <xsl:value-of select="cmd:rightsHolder"></xsl:value-of>
      </dct:rightsHolder>
    </xsl:if>
    <xsl:if test="cmd:source!=''">
      <dc:source>
        <xsl:value-of select="cmd:source"></xsl:value-of>
      </dc:source>
    </xsl:if>
    <xsl:if test="cmd:spatial!=''">
      <dct:spatial>
        <xsl:value-of select="cmd:spatial"></xsl:value-of>
      </dct:spatial>
    </xsl:if>
    <xsl:if test="cmd:subject!=''">
      <dc:subject>
        <xsl:value-of select="cmd:subject"></xsl:value-of>
      </dc:subject>
    </xsl:if>
    <xsl:if test="cmd:tableOfContents!=''">
      <dct:tableOfContents>
        <xsl:value-of select="cmd:tableOfContents"></xsl:value-of>
      </dct:tableOfContents>
    </xsl:if>
    <xsl:if test="cmd:temporal!=''">
      <dct:temporal>
        <xsl:value-of select="cmd:temporal"></xsl:value-of>
      </dct:temporal>
    </xsl:if>
    <xsl:if test="cmd:title!=''">
      <dc:title>
        <xsl:value-of select="cmd:title"></xsl:value-of>
      </dc:title>
    </xsl:if>
    <xsl:if test="cmd:type!=''">
      <dc:type>
        <xsl:value-of select="cmd:type"></xsl:value-of>
      </dc:type>
    </xsl:if>
    <xsl:if test="cmd:valid!=''">
      <dct:valid>
        <xsl:value-of select="cmd:valid"></xsl:value-of>
      </dct:valid>
    </xsl:if>
  </xsl:template>
  <xsl:template name="uri">
    <xsl:param name="u"></xsl:param>
    <xsl:choose>
      <xsl:when test="starts-with($u,'hdl:')">
        <xsl:attribute name="rdf:resource">
          <xsl:value-of select="concat('http://hdl.handle.net/', substring-after($u, 'hdl:'))"></xsl:value-of>
        </xsl:attribute>
      </xsl:when>
      <xsl:otherwise>
        <xsl:attribute name="rdf:resource">
          <xsl:value-of select="$u"></xsl:value-of>
        </xsl:attribute>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
</xsl:stylesheet>