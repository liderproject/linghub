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
    <xsl:if test="cmd:description!=''">
      <dc:description>
        <xsl:value-of select="cmd:description"></xsl:value-of>
      </dc:description>
    </xsl:if>
    <xsl:if test="cmd:format!=''">
      <dc:format>
        <xsl:value-of select="cmd:format"></xsl:value-of>
      </dc:format>
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
    <xsl:if test="cmd:language!=''">
      <dc:language>
        <xsl:value-of select="cmd:language"></xsl:value-of>
      </dc:language>
    </xsl:if>
    <xsl:if test="cmd:publisher!=''">
      <dc:publisher>
        <xsl:value-of select="cmd:publisher"></xsl:value-of>
      </dc:publisher>
    </xsl:if>
    <xsl:if test="cmd:rights!=''">
      <dc:rights>
        <xsl:value-of select="cmd:rights"></xsl:value-of>
      </dc:rights>
    </xsl:if>
    <xsl:if test="cmd:source!=''">
      <dc:source>
        <xsl:value-of select="cmd:source"></xsl:value-of>
      </dc:source>
    </xsl:if>
    <xsl:if test="cmd:subject!=''">
      <dc:subject>
        <xsl:value-of select="cmd:subject"></xsl:value-of>
      </dc:subject>
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