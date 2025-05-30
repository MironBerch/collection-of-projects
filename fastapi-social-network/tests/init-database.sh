#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
  CREATE TABLE countries (
    id SERIAL PRIMARY KEY,
    name TEXT,
    alpha2 TEXT,
    alpha3 TEXT,
    region TEXT
  );

  -- https://github.com/lukes/ISO-3166-Countries-with-Regional-Codes/blob/master/all/all.json
  -- cat tests/countries.json| jq '.[] | [.name, ."alpha-2", ."alpha-3", .region] | @csv' -r | tr "'" " " | tr '"' "'" | awk -F "\n" '{print "("$1"),"}'
  INSERT INTO countries (name, alpha2, alpha3, region) VALUES
  ('Afghanistan','AF','AFG','Asia'),
  ('Åland Islands','AX','ALA','Europe'),
  ('Albania','AL','ALB','Europe'),
  ('Algeria','DZ','DZA','Africa'),
  ('American Samoa','AS','ASM','Oceania'),
  ('Andorra','AD','AND','Europe'),
  ('Angola','AO','AGO','Africa'),
  ('Anguilla','AI','AIA','Americas'),
  ('Antigua and Barbuda','AG','ATG','Americas'),
  ('Argentina','AR','ARG','Americas'),
  ('Armenia','AM','ARM','Asia'),
  ('Aruba','AW','ABW','Americas'),
  ('Australia','AU','AUS','Oceania'),
  ('Austria','AT','AUT','Europe'),
  ('Azerbaijan','AZ','AZE','Asia'),
  ('Bahamas','BS','BHS','Americas'),
  ('Bahrain','BH','BHR','Asia'),
  ('Bangladesh','BD','BGD','Asia'),
  ('Barbados','BB','BRB','Americas'),
  ('Belarus','BY','BLR','Europe'),
  ('Belgium','BE','BEL','Europe'),
  ('Belize','BZ','BLZ','Americas'),
  ('Benin','BJ','BEN','Africa'),
  ('Bermuda','BM','BMU','Americas'),
  ('Bhutan','BT','BTN','Asia'),
  ('Bolivia (Plurinational State of)','BO','BOL','Americas'),
  ('Bonaire, Sint Eustatius and Saba','BQ','BES','Americas'),
  ('Bosnia and Herzegovina','BA','BIH','Europe'),
  ('Botswana','BW','BWA','Africa'),
  ('Bouvet Island','BV','BVT','Americas'),
  ('Brazil','BR','BRA','Americas'),
  ('British Indian Ocean Territory','IO','IOT','Africa'),
  ('Brunei Darussalam','BN','BRN','Asia'),
  ('Bulgaria','BG','BGR','Europe'),
  ('Burkina Faso','BF','BFA','Africa'),
  ('Burundi','BI','BDI','Africa'),
  ('Cabo Verde','CV','CPV','Africa'),
  ('Cambodia','KH','KHM','Asia'),
  ('Cameroon','CM','CMR','Africa'),
  ('Canada','CA','CAN','Americas'),
  ('Cayman Islands','KY','CYM','Americas'),
  ('Central African Republic','CF','CAF','Africa'),
  ('Chad','TD','TCD','Africa'),
  ('Chile','CL','CHL','Americas'),
  ('China','CN','CHN','Asia'),
  ('Christmas Island','CX','CXR','Oceania'),
  ('Cocos (Keeling) Islands','CC','CCK','Oceania'),
  ('Colombia','CO','COL','Americas'),
  ('Comoros','KM','COM','Africa'),
  ('Congo','CG','COG','Africa'),
  ('Congo, Democratic Republic of the','CD','COD','Africa'),
  ('Cook Islands','CK','COK','Oceania'),
  ('Costa Rica','CR','CRI','Americas'),
  ('Croatia','HR','HRV','Europe'),
  ('Cuba','CU','CUB','Americas'),
  ('Curaçao','CW','CUW','Americas'),
  ('Cyprus','CY','CYP','Asia'),
  ('Czechia','CZ','CZE','Europe'),
  ('Denmark','DK','DNK','Europe'),
  ('Djibouti','DJ','DJI','Africa'),
  ('Dominica','DM','DMA','Americas'),
  ('Dominican Republic','DO','DOM','Americas'),
  ('Ecuador','EC','ECU','Americas'),
  ('Egypt','EG','EGY','Africa'),
  ('El Salvador','SV','SLV','Americas'),
  ('Equatorial Guinea','GQ','GNQ','Africa'),
  ('Eritrea','ER','ERI','Africa'),
  ('Estonia','EE','EST','Europe'),
  ('Eswatini','SZ','SWZ','Africa'),
  ('Ethiopia','ET','ETH','Africa'),
  ('Falkland Islands (Malvinas)','FK','FLK','Americas'),
  ('Faroe Islands','FO','FRO','Europe'),
  ('Fiji','FJ','FJI','Oceania'),
  ('Finland','FI','FIN','Europe'),
  ('France','FR','FRA','Europe'),
  ('French Guiana','GF','GUF','Americas'),
  ('French Polynesia','PF','PYF','Oceania'),
  ('French Southern Territories','TF','ATF','Africa'),
  ('Gabon','GA','GAB','Africa'),
  ('Gambia','GM','GMB','Africa'),
  ('Georgia','GE','GEO','Asia'),
  ('Germany','DE','DEU','Europe'),
  ('Ghana','GH','GHA','Africa'),
  ('Gibraltar','GI','GIB','Europe'),
  ('Greece','GR','GRC','Europe'),
  ('Greenland','GL','GRL','Americas'),
  ('Grenada','GD','GRD','Americas'),
  ('Guadeloupe','GP','GLP','Americas'),
  ('Guam','GU','GUM','Oceania'),
  ('Guatemala','GT','GTM','Americas'),
  ('Guernsey','GG','GGY','Europe'),
  ('Guinea','GN','GIN','Africa'),
  ('Guinea-Bissau','GW','GNB','Africa'),
  ('Guyana','GY','GUY','Americas'),
  ('Haiti','HT','HTI','Americas'),
  ('Heard Island and McDonald Islands','HM','HMD','Oceania'),
  ('Holy See','VA','VAT','Europe'),
  ('Honduras','HN','HND','Americas'),
  ('Hong Kong','HK','HKG','Asia'),
  ('Hungary','HU','HUN','Europe'),
  ('Iceland','IS','ISL','Europe'),
  ('India','IN','IND','Asia'),
  ('Indonesia','ID','IDN','Asia'),
  ('Iran (Islamic Republic of)','IR','IRN','Asia'),
  ('Iraq','IQ','IRQ','Asia'),
  ('Ireland','IE','IRL','Europe'),
  ('Isle of Man','IM','IMN','Europe'),
  ('Israel','IL','ISR','Asia'),
  ('Italy','IT','ITA','Europe'),
  ('Jamaica','JM','JAM','Americas'),
  ('Japan','JP','JPN','Asia'),
  ('Jersey','JE','JEY','Europe'),
  ('Jordan','JO','JOR','Asia'),
  ('Kazakhstan','KZ','KAZ','Asia'),
  ('Kenya','KE','KEN','Africa'),
  ('Kiribati','KI','KIR','Oceania'),
  ('Korea, Republic of','KR','KOR','Asia'),
  ('Kuwait','KW','KWT','Asia'),
  ('Kyrgyzstan','KG','KGZ','Asia'),
  ('Latvia','LV','LVA','Europe'),
  ('Lebanon','LB','LBN','Asia'),
  ('Lesotho','LS','LSO','Africa'),
  ('Liberia','LR','LBR','Africa'),
  ('Libya','LY','LBY','Africa'),
  ('Liechtenstein','LI','LIE','Europe'),
  ('Lithuania','LT','LTU','Europe'),
  ('Luxembourg','LU','LUX','Europe'),
  ('Macao','MO','MAC','Asia'),
  ('Madagascar','MG','MDG','Africa'),
  ('Malawi','MW','MWI','Africa'),
  ('Malaysia','MY','MYS','Asia'),
  ('Maldives','MV','MDV','Asia'),
  ('Mali','ML','MLI','Africa'),
  ('Malta','MT','MLT','Europe'),
  ('Marshall Islands','MH','MHL','Oceania'),
  ('Martinique','MQ','MTQ','Americas'),
  ('Mauritania','MR','MRT','Africa'),
  ('Mauritius','MU','MUS','Africa'),
  ('Mayotte','YT','MYT','Africa'),
  ('Mexico','MX','MEX','Americas'),
  ('Micronesia (Federated States of)','FM','FSM','Oceania'),
  ('Moldova, Republic of','MD','MDA','Europe'),
  ('Monaco','MC','MCO','Europe'),
  ('Mongolia','MN','MNG','Asia'),
  ('Montenegro','ME','MNE','Europe'),
  ('Montserrat','MS','MSR','Americas'),
  ('Morocco','MA','MAR','Africa'),
  ('Mozambique','MZ','MOZ','Africa'),
  ('Myanmar','MM','MMR','Asia'),
  ('Namibia','NA','NAM','Africa'),
  ('Nauru','NR','NRU','Oceania'),
  ('Nepal','NP','NPL','Asia'),
  ('Netherlands','NL','NLD','Europe'),
  ('New Caledonia','NC','NCL','Oceania'),
  ('New Zealand','NZ','NZL','Oceania'),
  ('Nicaragua','NI','NIC','Americas'),
  ('Niger','NE','NER','Africa'),
  ('Nigeria','NG','NGA','Africa'),
  ('Niue','NU','NIU','Oceania'),
  ('Norfolk Island','NF','NFK','Oceania'),
  ('North Macedonia','MK','MKD','Europe'),
  ('Northern Mariana Islands','MP','MNP','Oceania'),
  ('Norway','NO','NOR','Europe'),
  ('Oman','OM','OMN','Asia'),
  ('Pakistan','PK','PAK','Asia'),
  ('Palau','PW','PLW','Oceania'),
  ('Palestine, State of','PS','PSE','Asia'),
  ('Panama','PA','PAN','Americas'),
  ('Papua New Guinea','PG','PNG','Oceania'),
  ('Paraguay','PY','PRY','Americas'),
  ('Peru','PE','PER','Americas'),
  ('Philippines','PH','PHL','Asia'),
  ('Pitcairn','PN','PCN','Oceania'),
  ('Poland','PL','POL','Europe'),
  ('Portugal','PT','PRT','Europe'),
  ('Puerto Rico','PR','PRI','Americas'),
  ('Qatar','QA','QAT','Asia'),
  ('Réunion','RE','REU','Africa'),
  ('Romania','RO','ROU','Europe'),
  ('Russian Federation','RU','RUS','Europe'),
  ('Rwanda','RW','RWA','Africa'),
  ('Saint Barthélemy','BL','BLM','Americas'),
  ('Saint Helena, Ascension and Tristan da Cunha','SH','SHN','Africa'),
  ('Saint Kitts and Nevis','KN','KNA','Americas'),
  ('Saint Lucia','LC','LCA','Americas'),
  ('Saint Martin (French part)','MF','MAF','Americas'),
  ('Saint Pierre and Miquelon','PM','SPM','Americas'),
  ('Saint Vincent and the Grenadines','VC','VCT','Americas'),
  ('Samoa','WS','WSM','Oceania'),
  ('San Marino','SM','SMR','Europe'),
  ('Sao Tome and Principe','ST','STP','Africa'),
  ('Saudi Arabia','SA','SAU','Asia'),
  ('Senegal','SN','SEN','Africa'),
  ('Serbia','RS','SRB','Europe'),
  ('Seychelles','SC','SYC','Africa'),
  ('Sierra Leone','SL','SLE','Africa'),
  ('Singapore','SG','SGP','Asia'),
  ('Sint Maarten (Dutch part)','SX','SXM','Americas'),
  ('Slovakia','SK','SVK','Europe'),
  ('Slovenia','SI','SVN','Europe'),
  ('Solomon Islands','SB','SLB','Oceania'),
  ('Somalia','SO','SOM','Africa'),
  ('South Africa','ZA','ZAF','Africa'),
  ('South Georgia and the South Sandwich Islands','GS','SGS','Americas'),
  ('South Sudan','SS','SSD','Africa'),
  ('Spain','ES','ESP','Europe'),
  ('Sri Lanka','LK','LKA','Asia'),
  ('Sudan','SD','SDN','Africa'),
  ('Suriname','SR','SUR','Americas'),
  ('Svalbard and Jan Mayen','SJ','SJM','Europe'),
  ('Sweden','SE','SWE','Europe'),
  ('Switzerland','CH','CHE','Europe'),
  ('Syrian Arab Republic','SY','SYR','Asia'),
  ('Taiwan, Province of China','TW','TWN','Asia'),
  ('Tajikistan','TJ','TJK','Asia'),
  ('Tanzania, United Republic of','TZ','TZA','Africa'),
  ('Thailand','TH','THA','Asia'),
  ('Timor-Leste','TL','TLS','Asia'),
  ('Togo','TG','TGO','Africa'),
  ('Tokelau','TK','TKL','Oceania'),
  ('Tonga','TO','TON','Oceania'),
  ('Trinidad and Tobago','TT','TTO','Americas'),
  ('Tunisia','TN','TUN','Africa'),
  ('Turkey','TR','TUR','Asia'),
  ('Turkmenistan','TM','TKM','Asia'),
  ('Turks and Caicos Islands','TC','TCA','Americas'),
  ('Tuvalu','TV','TUV','Oceania'),
  ('Uganda','UG','UGA','Africa'),
  ('Ukraine','UA','UKR','Europe'),
  ('United Arab Emirates','AE','ARE','Asia'),
  ('United Kingdom of Great Britain and Northern Ireland','GB','GBR','Europe'),
  ('United States of America','US','USA','Americas'),
  ('United States Minor Outlying Islands','UM','UMI','Oceania'),
  ('Uruguay','UY','URY','Americas'),
  ('Uzbekistan','UZ','UZB','Asia'),
  ('Vanuatu','VU','VUT','Oceania'),
  ('Venezuela (Bolivarian Republic of)','VE','VEN','Americas'),
  ('Viet Nam','VN','VNM','Asia'),
  ('Virgin Islands (British)','VG','VGB','Americas'),
  ('Virgin Islands (U.S.)','VI','VIR','Americas'),
  ('Wallis and Futuna','WF','WLF','Oceania'),
  ('Western Sahara','EH','ESH','Africa'),
  ('Yemen','YE','YEM','Asia'),
  ('Zambia','ZM','ZMB','Africa'),
  ('Zimbabwe','ZW','ZWE','Africa'),
  ('Byteland PROD','YY','YYY','Europe');
EOSQL
