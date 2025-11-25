## 🗂️ Treemap del Proyecto

```
├── .gitignore
├── app.py
├── config/
│   ├── paths.py
│   └── settings.json
├── controllers/
│   ├── app_controller.py
│   ├── certificates_controller.py
│   └── etl_controller.py
├── core/
│   ├── certificates/
│   │   ├── batch_processor.py
│   │   ├── data_filter.py
│   │   ├── pdf_converter.py
│   │   ├── validator.py
│   │   └── word_generator.py
│   ├── etl/
│   │   ├── contract_splitter.py
│   │   ├── data_cleaner.py
│   │   ├── data_loader.py
│   │   ├── date_processor.py
│   │   ├── etl_service.py
│   │   ├── file_generator.py
│   │   └── period_consolidator.py
│   └── utils/
│       ├── file_utils.py
│       └── logger.py
├── data/
│   ├── clean/
│   │   ├── .gitkeep
│   │   ├── clean_18.11.2025_09.45.02.xlsx
│   │   ├── clean_18.11.2025_10.00.14.xlsx
│   │   ├── clean_18.11.2025_10.53.10.xlsx
│   │   ├── clean_18.11.2025_11.35.40.xlsx
│   │   ├── clean_18.11.2025_11.41.25.xlsx
│   │   ├── clean_18.11.2025_12.08.14.xlsx
│   │   ├── clean_18.11.2025_12.10.10.xlsx
│   │   ├── clean_19.11.2025_11.20.20.xlsx
│   │   ├── clean_19.11.2025_11.48.38.xlsx
│   │   ├── clean_19.11.2025_12.04.45.xlsx
│   │   ├── clean_19.11.2025_12.16.38.xlsx
│   │   ├── clean_19.11.2025_12.20.29.xlsx
│   │   ├── clean_19.11.2025_12.28.59.xlsx
│   │   ├── clean_19.11.2025_14.17.06.xlsx
│   │   ├── clean_19.11.2025_14.46.59.xlsx
│   │   ├── clean_19.11.2025_15.18.42.xlsx
│   │   ├── clean_19.11.2025_16.57.29.xlsx
│   │   ├── clean_19.11.2025_17.50.47.xlsx
│   │   ├── clean_20.11.2025_14.22.17.xlsx
│   │   ├── clean_20.11.2025_14.31.20.xlsx
│   │   ├── clean_20.11.2025_14.47.03.xlsx
│   │   ├── clean_20.11.2025_14.56.48.xlsx
│   │   ├── clean_20.11.2025_15.09.03.xlsx
│   │   ├── clean_20251117_175341.xlsx
│   │   └── clean_21.11.2025_13.05.03.xlsx
│   ├── output/
│   │   ├── certificates_21.11.2025_13.28.24/
│   │   │   ├── pdf/
│   │   │   └── word/
│   │   │       ├── Certificado_ACUÑA MEZA CARLOS VICTOR.docx
│   │   │       ├── Certificado_ACUÑA MEZA CARLOS VICTOR_1.docx
│   │   │       ├── Certificado_ACUÑA MEZA CARLOS VICTOR_2.docx
│   │   │       ├── Certificado_ACUÑA MEZA CARLOS VICTOR_3.docx
│   │   │       ├── Certificado_AGUILAR CALSIN ROGER RESARDO.docx
│   │   │       ├── Certificado_AGUILAR CALSIN ROGER RESARDO_1.docx
│   │   │       ├── Certificado_AGUILAR CALSIN ROGER RESARDO_2.docx
│   │   │       ├── Certificado_AGUILAR CALSIN ROGER RESARDO_3.docx
│   │   │       ├── Certificado_AGUILAR NINA ELVER WALDEMAR.docx
│   │   │       ├── Certificado_AGUILAR NINA ELVER WALDEMAR_1.docx
│   │   │       ├── Certificado_AGUILAR NINA ELVER WALDEMAR_10.docx
│   │   │       ├── Certificado_AGUILAR NINA ELVER WALDEMAR_11.docx
│   │   │       ├── Certificado_AGUILAR NINA ELVER WALDEMAR_12.docx
│   │   │       ├── Certificado_AGUILAR NINA ELVER WALDEMAR_2.docx
│   │   │       ├── Certificado_AGUILAR NINA ELVER WALDEMAR_3.docx
│   │   │       ├── Certificado_AGUILAR NINA ELVER WALDEMAR_4.docx
│   │   │       ├── Certificado_AGUILAR NINA ELVER WALDEMAR_5.docx
│   │   │       ├── Certificado_AGUILAR NINA ELVER WALDEMAR_6.docx
│   │   │       ├── Certificado_AGUILAR NINA ELVER WALDEMAR_7.docx
│   │   │       ├── Certificado_AGUILAR NINA ELVER WALDEMAR_8.docx
│   │   │       ├── Certificado_AGUILAR NINA ELVER WALDEMAR_9.docx
│   │   │       ├── Certificado_AGURTO RIVERA DANIEL.docx
│   │   │       ├── Certificado_AGURTO RIVERA DANIEL_1.docx
│   │   │       ├── Certificado_AGURTO RIVERA DANIEL_2.docx
│   │   │       ├── Certificado_AGURTO RIVERA DANIEL_3.docx
│   │   │       ├── Certificado_AGURTO RIVERA DANIEL_4.docx
│   │   │       ├── Certificado_AGURTO RIVERA DANIEL_5.docx
│   │   │       ├── Certificado_AGURTO RIVERA DANIEL_6.docx
│   │   │       ├── Certificado_ANAYA COTRINA PAULINO MARCIAL.docx
│   │   │       ├── Certificado_ANAYA COTRINA PAULINO MARCIAL_1.docx
│   │   │       ├── Certificado_ANAYA COTRINA PAULINO MARCIAL_2.docx
│   │   │       ├── Certificado_ANAYA COTRINA PAULINO MARCIAL_3.docx
│   │   │       ├── Certificado_ANAYA COTRINA PAULINO MARCIAL_4.docx
│   │   │       ├── Certificado_ANAYA COTRINA PAULINO MARCIAL_5.docx
│   │   │       ├── Certificado_ARANA RABANAL WILLIAMS GILBERTO.docx
│   │   │       ├── Certificado_ARANCIBIA MINAYA WILMER.docx
│   │   │       ├── Certificado_ARANCIBIA MINAYA WILMER_1.docx
│   │   │       ├── Certificado_ARANCIBIA MINAYA WILMER_10.docx
│   │   │       ├── Certificado_ARANCIBIA MINAYA WILMER_11.docx
│   │   │       ├── Certificado_ARANCIBIA MINAYA WILMER_2.docx
│   │   │       ├── Certificado_ARANCIBIA MINAYA WILMER_3.docx
│   │   │       ├── Certificado_ARANCIBIA MINAYA WILMER_4.docx
│   │   │       ├── Certificado_ARANCIBIA MINAYA WILMER_5.docx
│   │   │       ├── Certificado_ARANCIBIA MINAYA WILMER_6.docx
│   │   │       ├── Certificado_ARANCIBIA MINAYA WILMER_7.docx
│   │   │       ├── Certificado_ARANCIBIA MINAYA WILMER_8.docx
│   │   │       ├── Certificado_ARANCIBIA MINAYA WILMER_9.docx
│   │   │       ├── Certificado_ARAPA QUISPE JOSE ANTONIO.docx
│   │   │       ├── Certificado_ARISPE CHUYACAMA JOSE ARMANDO.docx
│   │   │       ├── Certificado_ARISPE CHUYACAMA JOSE ARMANDO_1.docx
│   │   │       ├── Certificado_ARISPE CHUYACAMA JOSE ARMANDO_2.docx
│   │   │       ├── Certificado_ARISPE CHUYACAMA JOSE ARMANDO_3.docx
│   │   │       ├── Certificado_ARISPE CHUYACAMA JOSE ARMANDO_4.docx
│   │   │       ├── Certificado_ARISPE CHUYACAMA JOSE ARMANDO_5.docx
│   │   │       ├── Certificado_ARISPE CHUYACAMA JOSE ARMANDO_6.docx
│   │   │       ├── Certificado_ARISPE CHUYACAMA JOSE ARMANDO_7.docx
│   │   │       ├── Certificado_AVENDAÑO FLORES CARLOS RENE.docx
│   │   │       ├── Certificado_AVENDAÑO FLORES CARLOS RENE_1.docx
│   │   │       ├── Certificado_AVENDAÑO FLORES CARLOS RENE_10.docx
│   │   │       ├── Certificado_AVENDAÑO FLORES CARLOS RENE_11.docx
│   │   │       ├── Certificado_AVENDAÑO FLORES CARLOS RENE_12.docx
│   │   │       ├── Certificado_AVENDAÑO FLORES CARLOS RENE_13.docx
│   │   │       ├── Certificado_AVENDAÑO FLORES CARLOS RENE_2.docx
│   │   │       ├── Certificado_AVENDAÑO FLORES CARLOS RENE_3.docx
│   │   │       ├── Certificado_AVENDAÑO FLORES CARLOS RENE_4.docx
│   │   │       ├── Certificado_AVENDAÑO FLORES CARLOS RENE_5.docx
│   │   │       ├── Certificado_AVENDAÑO FLORES CARLOS RENE_6.docx
│   │   │       ├── Certificado_AVENDAÑO FLORES CARLOS RENE_7.docx
│   │   │       ├── Certificado_AVENDAÑO FLORES CARLOS RENE_8.docx
│   │   │       ├── Certificado_AVENDAÑO FLORES CARLOS RENE_9.docx
│   │   │       ├── Certificado_AYALA RIOS ANTONIO.docx
│   │   │       ├── Certificado_BARJA LARA PERCY.docx
│   │   │       ├── Certificado_BARJA LARA PERCY_1.docx
│   │   │       ├── Certificado_BARJA LARA PERCY_2.docx
│   │   │       ├── Certificado_BARJA LARA PERCY_3.docx
│   │   │       ├── Certificado_BARJA LARA PERCY_4.docx
│   │   │       ├── Certificado_BARJA LARA PERCY_5.docx
│   │   │       ├── Certificado_BARJA LARA PERCY_6.docx
│   │   │       ├── Certificado_BARJA LARA PERCY_7.docx
│   │   │       ├── Certificado_BARJA LARA PERCY_8.docx
│   │   │       ├── Certificado_BARRIOS FLORES DARWIN SANTIAGO.docx
│   │   │       ├── Certificado_BARRIOS FLORES DARWIN SANTIAGO_1.docx
│   │   │       ├── Certificado_BARRIOS FLORES DARWIN SANTIAGO_10.docx
│   │   │       ├── Certificado_BARRIOS FLORES DARWIN SANTIAGO_11.docx
│   │   │       ├── Certificado_BARRIOS FLORES DARWIN SANTIAGO_2.docx
│   │   │       ├── Certificado_BARRIOS FLORES DARWIN SANTIAGO_3.docx
│   │   │       ├── Certificado_BARRIOS FLORES DARWIN SANTIAGO_4.docx
│   │   │       ├── Certificado_BARRIOS FLORES DARWIN SANTIAGO_5.docx
│   │   │       ├── Certificado_BARRIOS FLORES DARWIN SANTIAGO_6.docx
│   │   │       ├── Certificado_BARRIOS FLORES DARWIN SANTIAGO_7.docx
│   │   │       ├── Certificado_BARRIOS FLORES DARWIN SANTIAGO_8.docx
│   │   │       ├── Certificado_BARRIOS FLORES DARWIN SANTIAGO_9.docx
│   │   │       ├── Certificado_BARRIOS HUACAC DANIEL.docx
│   │   │       ├── Certificado_BARRIOS HUACAC DANIEL_1.docx
│   │   │       ├── Certificado_BARRIOS HUACAC DANIEL_10.docx
│   │   │       ├── Certificado_BARRIOS HUACAC DANIEL_11.docx
│   │   │       ├── Certificado_BARRIOS HUACAC DANIEL_12.docx
│   │   │       ├── Certificado_BARRIOS HUACAC DANIEL_13.docx
│   │   │       ├── Certificado_BARRIOS HUACAC DANIEL_14.docx
│   │   │       ├── Certificado_BARRIOS HUACAC DANIEL_15.docx
│   │   │       ├── Certificado_BARRIOS HUACAC DANIEL_16.docx
│   │   │       ├── Certificado_BARRIOS HUACAC DANIEL_17.docx
│   │   │       ├── Certificado_BARRIOS HUACAC DANIEL_18.docx
│   │   │       ├── Certificado_BARRIOS HUACAC DANIEL_2.docx
│   │   │       ├── Certificado_BARRIOS HUACAC DANIEL_3.docx
│   │   │       ├── Certificado_BARRIOS HUACAC DANIEL_4.docx
│   │   │       ├── Certificado_BARRIOS HUACAC DANIEL_5.docx
│   │   │       ├── Certificado_BARRIOS HUACAC DANIEL_6.docx
│   │   │       ├── Certificado_BARRIOS HUACAC DANIEL_7.docx
│   │   │       ├── Certificado_BARRIOS HUACAC DANIEL_8.docx
│   │   │       ├── Certificado_BARRIOS HUACAC DANIEL_9.docx
│   │   │       ├── Certificado_BAZAN CHAVEZ JOSE ALEJANDRO.docx
│   │   │       ├── Certificado_BAZAN CHAVEZ JOSE ALEJANDRO_1.docx
│   │   │       ├── Certificado_BAZAN CHAVEZ JOSE ALEJANDRO_2.docx
│   │   │       ├── Certificado_BAZAN CHAVEZ JOSE ALEJANDRO_3.docx
│   │   │       ├── Certificado_BAZAN CHAVEZ JOSE ALEJANDRO_4.docx
│   │   │       ├── Certificado_BAZAN CHAVEZ JOSE ALEJANDRO_5.docx
│   │   │       ├── Certificado_BAZAN CHAVEZ JOSE ALEJANDRO_6.docx
│   │   │       ├── Certificado_BAZAN CHAVEZ JOSE ALEJANDRO_7.docx
│   │   │       ├── Certificado_BAZAN CHAVEZ JOSE ALEJANDRO_8.docx
│   │   │       ├── Certificado_BAZAN CHAVEZ JOSE ALEJANDRO_9.docx
│   │   │       ├── Certificado_BORDA SONCCO ENRIQUE.docx
│   │   │       ├── Certificado_BORDA SONCCO ENRIQUE_1.docx
│   │   │       ├── Certificado_BORDA SONCCO ENRIQUE_10.docx
│   │   │       ├── Certificado_BORDA SONCCO ENRIQUE_11.docx
│   │   │       ├── Certificado_BORDA SONCCO ENRIQUE_12.docx
│   │   │       ├── Certificado_BORDA SONCCO ENRIQUE_13.docx
│   │   │       ├── Certificado_BORDA SONCCO ENRIQUE_14.docx
│   │   │       ├── Certificado_BORDA SONCCO ENRIQUE_15.docx
│   │   │       ├── Certificado_BORDA SONCCO ENRIQUE_16.docx
│   │   │       ├── Certificado_BORDA SONCCO ENRIQUE_17.docx
│   │   │       ├── Certificado_BORDA SONCCO ENRIQUE_18.docx
│   │   │       ├── Certificado_BORDA SONCCO ENRIQUE_19.docx
│   │   │       ├── Certificado_BORDA SONCCO ENRIQUE_2.docx
│   │   │       ├── Certificado_BORDA SONCCO ENRIQUE_20.docx
│   │   │       ├── Certificado_BORDA SONCCO ENRIQUE_21.docx
│   │   │       ├── Certificado_BORDA SONCCO ENRIQUE_22.docx
│   │   │       ├── Certificado_BORDA SONCCO ENRIQUE_23.docx
│   │   │       ├── Certificado_BORDA SONCCO ENRIQUE_24.docx
│   │   │       ├── Certificado_BORDA SONCCO ENRIQUE_25.docx
│   │   │       ├── Certificado_BORDA SONCCO ENRIQUE_26.docx
│   │   │       ├── Certificado_BORDA SONCCO ENRIQUE_27.docx
│   │   │       ├── Certificado_BORDA SONCCO ENRIQUE_28.docx
│   │   │       ├── Certificado_BORDA SONCCO ENRIQUE_29.docx
│   │   │       ├── Certificado_BORDA SONCCO ENRIQUE_3.docx
│   │   │       ├── Certificado_BORDA SONCCO ENRIQUE_4.docx
│   │   │       ├── Certificado_BORDA SONCCO ENRIQUE_5.docx
│   │   │       ├── Certificado_BORDA SONCCO ENRIQUE_6.docx
│   │   │       ├── Certificado_BORDA SONCCO ENRIQUE_7.docx
│   │   │       ├── Certificado_BORDA SONCCO ENRIQUE_8.docx
│   │   │       ├── Certificado_BORDA SONCCO ENRIQUE_9.docx
│   │   │       ├── Certificado_BRAVO CASTELLO ENRIQUE LEONCIO.docx
│   │   │       ├── Certificado_BRUNO MORALES EVER.docx
│   │   │       ├── Certificado_BRUNO MORALES EVER_1.docx
│   │   │       ├── Certificado_BRUNO MORALES EVER_10.docx
│   │   │       ├── Certificado_BRUNO MORALES EVER_11.docx
│   │   │       ├── Certificado_BRUNO MORALES EVER_12.docx
│   │   │       ├── Certificado_BRUNO MORALES EVER_13.docx
│   │   │       ├── Certificado_BRUNO MORALES EVER_14.docx
│   │   │       ├── Certificado_BRUNO MORALES EVER_15.docx
│   │   │       ├── Certificado_BRUNO MORALES EVER_2.docx
│   │   │       ├── Certificado_BRUNO MORALES EVER_3.docx
│   │   │       ├── Certificado_BRUNO MORALES EVER_4.docx
│   │   │       ├── Certificado_BRUNO MORALES EVER_5.docx
│   │   │       ├── Certificado_BRUNO MORALES EVER_6.docx
│   │   │       ├── Certificado_BRUNO MORALES EVER_7.docx
│   │   │       ├── Certificado_BRUNO MORALES EVER_8.docx
│   │   │       ├── Certificado_BRUNO MORALES EVER_9.docx
│   │   │       ├── Certificado_BUENO JUAN DE DIOS ELIAS DAVID.docx
│   │   │       ├── Certificado_BUENO JUAN DE DIOS ELIAS DAVID_1.docx
│   │   │       ├── Certificado_CABRERA CANO GONZALO DAMASO.docx
│   │   │       ├── Certificado_CABRERA CANO GONZALO DAMASO_1.docx
│   │   │       ├── Certificado_CABRERA CANO GONZALO DAMASO_2.docx
│   │   │       ├── Certificado_CABRERA CANO GONZALO DAMASO_3.docx
│   │   │       ├── Certificado_CACERES CHINO MARGOT.docx
│   │   │       ├── Certificado_CACERES CHINO MARGOT_1.docx
│   │   │       ├── Certificado_CACHAY LEVANO WILLIAM ALBERTO.docx
│   │   │       ├── Certificado_CACHAY LEVANO WILLIAM ALBERTO_1.docx
│   │   │       ├── Certificado_CACHAY LEVANO WILLIAM ALBERTO_2.docx
│   │   │       ├── Certificado_CAJACURI INGA HENRY.docx
│   │   │       ├── Certificado_CAJACURI INGA HENRY_1.docx
│   │   │       ├── Certificado_CAJACURI INGA HENRY_10.docx
│   │   │       ├── Certificado_CAJACURI INGA HENRY_2.docx
│   │   │       ├── Certificado_CAJACURI INGA HENRY_3.docx
│   │   │       ├── Certificado_CAJACURI INGA HENRY_4.docx
│   │   │       ├── Certificado_CAJACURI INGA HENRY_5.docx
│   │   │       ├── Certificado_CAJACURI INGA HENRY_6.docx
│   │   │       ├── Certificado_CAJACURI INGA HENRY_7.docx
│   │   │       ├── Certificado_CAJACURI INGA HENRY_8.docx
│   │   │       ├── Certificado_CAJACURI INGA HENRY_9.docx
│   │   │       ├── Certificado_CALLA QUISPE IVAN EDWIN.docx
│   │   │       ├── Certificado_CAMONES HUAÑEC GILBER PASCUAL.docx
│   │   │       ├── Certificado_CAMONES HUAÑEC GILBER PASCUAL_1.docx
│   │   │       ├── Certificado_CAMONES HUAÑEC GILBER PASCUAL_10.docx
│   │   │       ├── Certificado_CAMONES HUAÑEC GILBER PASCUAL_11.docx
│   │   │       ├── Certificado_CAMONES HUAÑEC GILBER PASCUAL_12.docx
│   │   │       ├── Certificado_CAMONES HUAÑEC GILBER PASCUAL_13.docx
│   │   │       ├── Certificado_CAMONES HUAÑEC GILBER PASCUAL_14.docx
│   │   │       ├── Certificado_CAMONES HUAÑEC GILBER PASCUAL_2.docx
│   │   │       ├── Certificado_CAMONES HUAÑEC GILBER PASCUAL_3.docx
│   │   │       ├── Certificado_CAMONES HUAÑEC GILBER PASCUAL_4.docx
│   │   │       ├── Certificado_CAMONES HUAÑEC GILBER PASCUAL_5.docx
│   │   │       ├── Certificado_CAMONES HUAÑEC GILBER PASCUAL_6.docx
│   │   │       ├── Certificado_CAMONES HUAÑEC GILBER PASCUAL_7.docx
│   │   │       ├── Certificado_CAMONES HUAÑEC GILBER PASCUAL_8.docx
│   │   │       ├── Certificado_CAMONES HUAÑEC GILBER PASCUAL_9.docx
│   │   │       ├── Certificado_CAMPOS MORE JOSE LUIS.docx
│   │   │       ├── Certificado_CAMPOS MORE JOSE LUIS_1.docx
│   │   │       ├── Certificado_CAMPOSANO QUISPE RIGOBERTO CARLOS.docx
│   │   │       ├── Certificado_CAMPOSANO QUISPE RIGOBERTO CARLOS_1.docx
│   │   │       ├── Certificado_CAMPOSANO QUISPE RIGOBERTO CARLOS_2.docx
│   │   │       ├── Certificado_CAMPOSANO QUISPE RIGOBERTO CARLOS_3.docx
│   │   │       ├── Certificado_CAMPOSANO QUISPE RIGOBERTO CARLOS_4.docx
│   │   │       ├── Certificado_CAMPOSANO QUISPE RIGOBERTO CARLOS_5.docx
│   │   │       ├── Certificado_CAMPOSANO QUISPE RIGOBERTO CARLOS_6.docx
│   │   │       ├── Certificado_CAMPOSANO QUISPE RIGOBERTO CARLOS_7.docx
│   │   │       ├── Certificado_CAMPOSANO QUISPE RIGOBERTO CARLOS_8.docx
│   │   │       ├── Certificado_CANDIA TORRES REMBER YOSET.docx
│   │   │       ├── Certificado_CARDENAS HUAMAN RAUL.docx
│   │   │       ├── Certificado_CARDENAS SANTISTEBAN JUAN ANTONIO.docx
│   │   │       ├── Certificado_CARDENAS SANTISTEBAN JUAN ANTONIO_1.docx
│   │   │       ├── Certificado_CARDENAS SANTISTEBAN JUAN ANTONIO_2.docx
│   │   │       ├── Certificado_CARDENAS SANTISTEBAN JUAN ANTONIO_3.docx
│   │   │       ├── Certificado_CARDENAS SANTISTEBAN JUAN ANTONIO_4.docx
│   │   │       ├── Certificado_CARDENAS SANTISTEBAN JUAN ANTONIO_5.docx
│   │   │       ├── Certificado_CARDENAS SANTISTEBAN JUAN ANTONIO_6.docx
│   │   │       ├── Certificado_CARDENAS SANTISTEBAN JUAN ANTONIO_7.docx
│   │   │       ├── Certificado_CARDENAS SANTISTEBAN JUAN ANTONIO_8.docx
│   │   │       ├── Certificado_CARDENAS SANTISTEBAN JUAN ANTONIO_9.docx
│   │   │       ├── Certificado_CASANI TOLEDO PEDRO.docx
│   │   │       ├── Certificado_CASTILLO SUDARIO ANGEL ROBERT.docx
│   │   │       ├── Certificado_CAYO POCOHUANCA BENJAMIN JUAN.docx
│   │   │       ├── Certificado_CAYO POCOHUANCA BENJAMIN JUAN_1.docx
│   │   │       ├── Certificado_CAYO POCOHUANCA BENJAMIN JUAN_2.docx
│   │   │       ├── Certificado_CAYO POCOHUANCA BENJAMIN JUAN_3.docx
│   │   │       ├── Certificado_CAYO POCOHUANCA BENJAMIN JUAN_4.docx
│   │   │       ├── Certificado_CAYO POCOHUANCA BENJAMIN JUAN_5.docx
│   │   │       ├── Certificado_CAYO POCOHUANCA BENJAMIN JUAN_6.docx
│   │   │       ├── Certificado_CAYO POCOHUANCA BENJAMIN JUAN_7.docx
│   │   │       ├── Certificado_CAYRO ARMEJO JIM GIOVANNI.docx
│   │   │       ├── Certificado_CAYRO ARMEJO JIM GIOVANNI_1.docx
│   │   │       ├── Certificado_CAYRO ARMEJO JIM GIOVANNI_10.docx
│   │   │       ├── Certificado_CAYRO ARMEJO JIM GIOVANNI_11.docx
│   │   │       ├── Certificado_CAYRO ARMEJO JIM GIOVANNI_2.docx
│   │   │       ├── Certificado_CAYRO ARMEJO JIM GIOVANNI_3.docx
│   │   │       ├── Certificado_CAYRO ARMEJO JIM GIOVANNI_4.docx
│   │   │       ├── Certificado_CAYRO ARMEJO JIM GIOVANNI_5.docx
│   │   │       ├── Certificado_CAYRO ARMEJO JIM GIOVANNI_6.docx
│   │   │       ├── Certificado_CAYRO ARMEJO JIM GIOVANNI_7.docx
│   │   │       ├── Certificado_CAYRO ARMEJO JIM GIOVANNI_8.docx
│   │   │       ├── Certificado_CAYRO ARMEJO JIM GIOVANNI_9.docx
│   │   │       ├── Certificado_CCOTO CACERES JUAN CARLOS.docx
│   │   │       ├── Certificado_CCOTO CACERES JUAN CARLOS_1.docx
│   │   │       ├── Certificado_CCOTO CACERES JUAN CARLOS_10.docx
│   │   │       ├── Certificado_CCOTO CACERES JUAN CARLOS_11.docx
│   │   │       ├── Certificado_CCOTO CACERES JUAN CARLOS_12.docx
│   │   │       ├── Certificado_CCOTO CACERES JUAN CARLOS_13.docx
│   │   │       ├── Certificado_CCOTO CACERES JUAN CARLOS_14.docx
│   │   │       ├── Certificado_CCOTO CACERES JUAN CARLOS_15.docx
│   │   │       ├── Certificado_CCOTO CACERES JUAN CARLOS_16.docx
│   │   │       ├── Certificado_CCOTO CACERES JUAN CARLOS_17.docx
│   │   │       ├── Certificado_CCOTO CACERES JUAN CARLOS_18.docx
│   │   │       ├── Certificado_CCOTO CACERES JUAN CARLOS_19.docx
│   │   │       ├── Certificado_CCOTO CACERES JUAN CARLOS_2.docx
│   │   │       ├── Certificado_CCOTO CACERES JUAN CARLOS_20.docx
│   │   │       ├── Certificado_CCOTO CACERES JUAN CARLOS_21.docx
│   │   │       ├── Certificado_CCOTO CACERES JUAN CARLOS_22.docx
│   │   │       ├── Certificado_CCOTO CACERES JUAN CARLOS_23.docx
│   │   │       ├── Certificado_CCOTO CACERES JUAN CARLOS_24.docx
│   │   │       ├── Certificado_CCOTO CACERES JUAN CARLOS_25.docx
│   │   │       ├── Certificado_CCOTO CACERES JUAN CARLOS_3.docx
│   │   │       ├── Certificado_CCOTO CACERES JUAN CARLOS_4.docx
│   │   │       ├── Certificado_CCOTO CACERES JUAN CARLOS_5.docx
│   │   │       ├── Certificado_CCOTO CACERES JUAN CARLOS_6.docx
│   │   │       ├── Certificado_CCOTO CACERES JUAN CARLOS_7.docx
│   │   │       ├── Certificado_CCOTO CACERES JUAN CARLOS_8.docx
│   │   │       ├── Certificado_CCOTO CACERES JUAN CARLOS_9.docx
│   │   │       ├── Certificado_CHAHUA SALVADOR EINSTEIN.docx
│   │   │       ├── Certificado_CHAHUA SALVADOR EINSTEIN_1.docx
│   │   │       ├── Certificado_CHAHUA SALVADOR EINSTEIN_2.docx
│   │   │       ├── Certificado_CHAHUA SALVADOR EINSTEIN_3.docx
│   │   │       ├── Certificado_CHAHUA SALVADOR EINSTEIN_4.docx
│   │   │       ├── Certificado_CHANCASANAMPA ASTO IVAN ERNAN.docx
│   │   │       ├── Certificado_CHANCASANAMPA ASTO IVAN ERNAN_1.docx
│   │   │       ├── Certificado_CHANCASANAMPA ASTO IVAN ERNAN_2.docx
│   │   │       ├── Certificado_CHANCASANAMPA ASTO IVAN ERNAN_3.docx
│   │   │       ├── Certificado_CHANCASANAMPA ASTO IVAN ERNAN_4.docx
│   │   │       ├── Certificado_CHANCASANAMPA ASTO IVAN ERNAN_5.docx
│   │   │       ├── Certificado_CHANCASANAMPA ASTO IVAN ERNAN_6.docx
│   │   │       ├── Certificado_CHAVEZ GRIJALVA ZAIDA RUTH.docx
│   │   │       ├── Certificado_CHAVEZ GRIJALVA ZAIDA RUTH_1.docx
│   │   │       ├── Certificado_CHAVEZ GRIJALVA ZAIDA RUTH_2.docx
│   │   │       ├── Certificado_CHAVEZ GRIJALVA ZAIDA RUTH_3.docx
│   │   │       ├── Certificado_CHAVEZ MANIHUARI JORGE LUIS.docx
│   │   │       ├── Certificado_CHAVEZ MANIHUARI JORGE LUIS_1.docx
│   │   │       ├── Certificado_CHAVEZ PINTO RAUL ORLANDO.docx
│   │   │       ├── Certificado_CHAVEZ PINTO RAUL ORLANDO_1.docx
│   │   │       ├── Certificado_CHAVEZ PINTO RAUL ORLANDO_10.docx
│   │   │       ├── Certificado_CHAVEZ PINTO RAUL ORLANDO_11.docx
│   │   │       ├── Certificado_CHAVEZ PINTO RAUL ORLANDO_12.docx
│   │   │       ├── Certificado_CHAVEZ PINTO RAUL ORLANDO_13.docx
│   │   │       ├── Certificado_CHAVEZ PINTO RAUL ORLANDO_2.docx
│   │   │       ├── Certificado_CHAVEZ PINTO RAUL ORLANDO_3.docx
│   │   │       ├── Certificado_CHAVEZ PINTO RAUL ORLANDO_4.docx
│   │   │       ├── Certificado_CHAVEZ PINTO RAUL ORLANDO_5.docx
│   │   │       ├── Certificado_CHAVEZ PINTO RAUL ORLANDO_6.docx
│   │   │       ├── Certificado_CHAVEZ PINTO RAUL ORLANDO_7.docx
│   │   │       ├── Certificado_CHAVEZ PINTO RAUL ORLANDO_8.docx
│   │   │       ├── Certificado_CHAVEZ PINTO RAUL ORLANDO_9.docx
│   │   │       ├── Certificado_CHOQUEHUANCA MAMANI RICHARD ALEJANDRO.docx
│   │   │       ├── Certificado_CHOQUEHUANCA MAMANI RICHARD ALEJANDRO_1.docx
│   │   │       ├── Certificado_CHOQUEHUANCA MAMANI RICHARD ALEJANDRO_10.docx
│   │   │       ├── Certificado_CHOQUEHUANCA MAMANI RICHARD ALEJANDRO_11.docx
│   │   │       ├── Certificado_CHOQUEHUANCA MAMANI RICHARD ALEJANDRO_2.docx
│   │   │       ├── Certificado_CHOQUEHUANCA MAMANI RICHARD ALEJANDRO_3.docx
│   │   │       ├── Certificado_CHOQUEHUANCA MAMANI RICHARD ALEJANDRO_4.docx
│   │   │       ├── Certificado_CHOQUEHUANCA MAMANI RICHARD ALEJANDRO_5.docx
│   │   │       ├── Certificado_CHOQUEHUANCA MAMANI RICHARD ALEJANDRO_6.docx
│   │   │       ├── Certificado_CHOQUEHUANCA MAMANI RICHARD ALEJANDRO_7.docx
│   │   │       ├── Certificado_CHOQUEHUANCA MAMANI RICHARD ALEJANDRO_8.docx
│   │   │       ├── Certificado_CHOQUEHUANCA MAMANI RICHARD ALEJANDRO_9.docx
│   │   │       ├── Certificado_CHUCTAYA CRUZ FORTUNATO.docx
│   │   │       ├── Certificado_CHUCTAYA CRUZ FORTUNATO_1.docx
│   │   │       ├── Certificado_COA CABANA HUGO GABRIEL.docx
│   │   │       ├── Certificado_COLINA FIGGINI MARIA VERONICA.docx
│   │   │       ├── Certificado_COLINA FIGGINI MARIA VERONICA_1.docx
│   │   │       ├── Certificado_COLINA FIGGINI MARIA VERONICA_2.docx
│   │   │       ├── Certificado_COLINA FIGGINI MARIA VERONICA_3.docx
│   │   │       ├── Certificado_CONDORI APAZA RICARDO.docx
│   │   │       ├── Certificado_CONDORI CASTILLO EUGENIO ALBERTO.docx
│   │   │       ├── Certificado_CONDORI CASTILLO EUGENIO ALBERTO_1.docx
│   │   │       ├── Certificado_CONDORI CASTILLO EUGENIO ALBERTO_2.docx
│   │   │       ├── Certificado_CONDORI CASTILLO EUGENIO ALBERTO_3.docx
│   │   │       ├── Certificado_CONDORI CASTILLO EUGENIO ALBERTO_4.docx
│   │   │       ├── Certificado_CONDORI CASTILLO EUGENIO ALBERTO_5.docx
│   │   │       ├── Certificado_CONDORI CASTILLO EUGENIO ALBERTO_6.docx
│   │   │       ├── Certificado_CONDORI CASTILLO EUGENIO ALBERTO_7.docx
│   │   │       ├── Certificado_CONDORI CASTILLO EUGENIO ALBERTO_8.docx
│   │   │       ├── Certificado_CORNEJO GALLARDO CESAR MANUEL.docx
│   │   │       ├── Certificado_CORRALES FERNANDEZ LENNI TATIANA.docx
│   │   │       ├── Certificado_CORRALES FERNANDEZ LENNI TATIANA_1.docx
│   │   │       ├── Certificado_CRUZ MELENDREZ FELIZANDRO.docx
│   │   │       ├── Certificado_CRUZ MELENDREZ FELIZANDRO_1.docx
│   │   │       ├── Certificado_CRUZ MELENDREZ FELIZANDRO_2.docx
│   │   │       ├── Certificado_CRUZ MELENDREZ FELIZANDRO_3.docx
│   │   │       ├── Certificado_CRUZ MELENDREZ FELIZANDRO_4.docx
│   │   │       ├── Certificado_CRUZ MELENDREZ FELIZANDRO_5.docx
│   │   │       ├── Certificado_CRUZ MELENDREZ FELIZANDRO_6.docx
│   │   │       ├── Certificado_CRUZ MELENDREZ FELIZANDRO_7.docx
│   │   │       ├── Certificado_CRUZ MELENDREZ FELIZANDRO_8.docx
│   │   │       ├── Certificado_CRUZ MELENDREZ FELIZANDRO_9.docx
│   │   │       ├── Certificado_CURE CHAUCA JUAN RAYMUNDO.docx
│   │   │       ├── Certificado_CURE CHAUCA JUAN RAYMUNDO_1.docx
│   │   │       ├── Certificado_CUTIRE CONDORI FRANCISCO HOOVER.docx
│   │   │       ├── Certificado_CUTIRE CONDORI FRANCISCO HOOVER_1.docx
│   │   │       ├── Certificado_CUTIRE CONDORI FRANCISCO HOOVER_10.docx
│   │   │       ├── Certificado_CUTIRE CONDORI FRANCISCO HOOVER_11.docx
│   │   │       ├── Certificado_CUTIRE CONDORI FRANCISCO HOOVER_12.docx
│   │   │       ├── Certificado_CUTIRE CONDORI FRANCISCO HOOVER_13.docx
│   │   │       ├── Certificado_CUTIRE CONDORI FRANCISCO HOOVER_14.docx
│   │   │       ├── Certificado_CUTIRE CONDORI FRANCISCO HOOVER_15.docx
│   │   │       ├── Certificado_CUTIRE CONDORI FRANCISCO HOOVER_16.docx
│   │   │       ├── Certificado_CUTIRE CONDORI FRANCISCO HOOVER_17.docx
│   │   │       ├── Certificado_CUTIRE CONDORI FRANCISCO HOOVER_2.docx
│   │   │       ├── Certificado_CUTIRE CONDORI FRANCISCO HOOVER_3.docx
│   │   │       ├── Certificado_CUTIRE CONDORI FRANCISCO HOOVER_4.docx
│   │   │       ├── Certificado_CUTIRE CONDORI FRANCISCO HOOVER_5.docx
│   │   │       ├── Certificado_CUTIRE CONDORI FRANCISCO HOOVER_6.docx
│   │   │       ├── Certificado_CUTIRE CONDORI FRANCISCO HOOVER_7.docx
│   │   │       ├── Certificado_CUTIRE CONDORI FRANCISCO HOOVER_8.docx
│   │   │       ├── Certificado_CUTIRE CONDORI FRANCISCO HOOVER_9.docx
│   │   │       ├── Certificado_DAVILA ZAMBRANO HUBERT WILBERT.docx
│   │   │       ├── Certificado_DELGADO TICONA JESUS.docx
│   │   │       ├── Certificado_DIAZ MEZA LUIS.docx
│   │   │       ├── Certificado_DIAZ MEZA LUIS_1.docx
│   │   │       ├── Certificado_DIAZ MEZA LUIS_2.docx
│   │   │       ├── Certificado_DIAZ ROLDAN EDWIN GERMAIN.docx
│   │   │       ├── Certificado_DIAZ ROLDAN EDWIN GERMAIN_1.docx
│   │   │       ├── Certificado_ESPINOZA CABALLERO RAUL FERNANDO.docx
│   │   │       ├── Certificado_ESPINOZA CABALLERO RAUL FERNANDO_1.docx
│   │   │       ├── Certificado_ESPINOZA CABALLERO RAUL FERNANDO_2.docx
│   │   │       ├── Certificado_ESPINOZA CABALLERO RAUL FERNANDO_3.docx
│   │   │       ├── Certificado_ESPINOZA CABALLERO RAUL FERNANDO_4.docx
│   │   │       ├── Certificado_ESPINOZA CABALLERO RAUL FERNANDO_5.docx
│   │   │       ├── Certificado_ESPINOZA CABALLERO RAUL FERNANDO_6.docx
│   │   │       ├── Certificado_ESPINOZA CABALLERO RAUL FERNANDO_7.docx
│   │   │       ├── Certificado_ESPINOZA MUÑOZ ALDO MAGNO.docx
│   │   │       ├── Certificado_ESPINOZA MUÑOZ ALDO MAGNO_1.docx
│   │   │       ├── Certificado_ESPINOZA VILLANUEVA EDGAR.docx
│   │   │       ├── Certificado_ESPINOZA VILLANUEVA EDGAR_1.docx
│   │   │       ├── Certificado_ESPINOZA VILLANUEVA EDGAR_2.docx
│   │   │       ├── Certificado_ESPINOZA VILLANUEVA EDGAR_3.docx
│   │   │       ├── Certificado_ESPINOZA VILLANUEVA EDGAR_4.docx
│   │   │       ├── Certificado_ESPINOZA VILLANUEVA EDGAR_5.docx
│   │   │       ├── Certificado_ESPINOZA VILLANUEVA EDGAR_6.docx
│   │   │       ├── Certificado_FLORES FLORES RUBEN.docx
│   │   │       ├── Certificado_FLORES FLORES RUBEN_1.docx
│   │   │       ├── Certificado_FLORES FLORES RUBEN_2.docx
│   │   │       ├── Certificado_FLORES FLORES RUBEN_3.docx
│   │   │       ├── Certificado_FLORES FLORES RUBEN_4.docx
│   │   │       ├── Certificado_GALVEZ AMAYA LUIS RODOLFO.docx
│   │   │       ├── Certificado_GARCIA MARQUINA JORGE LUIS.docx
│   │   │       ├── Certificado_GARCIA MARQUINA JORGE LUIS_1.docx
│   │   │       ├── Certificado_GARCIA MARQUINA JORGE LUIS_2.docx
│   │   │       ├── Certificado_GARCIA MARQUINA JORGE LUIS_3.docx
│   │   │       ├── Certificado_GOMEZ CARPIO ALBERTO SAMUEL.docx
│   │   │       ├── Certificado_GOMEZ CARPIO ALBERTO SAMUEL_1.docx
│   │   │       ├── Certificado_GOMEZ CARPIO ALBERTO SAMUEL_10.docx
│   │   │       ├── Certificado_GOMEZ CARPIO ALBERTO SAMUEL_11.docx
│   │   │       ├── Certificado_GOMEZ CARPIO ALBERTO SAMUEL_12.docx
│   │   │       ├── Certificado_GOMEZ CARPIO ALBERTO SAMUEL_2.docx
│   │   │       ├── Certificado_GOMEZ CARPIO ALBERTO SAMUEL_3.docx
│   │   │       ├── Certificado_GOMEZ CARPIO ALBERTO SAMUEL_4.docx
│   │   │       ├── Certificado_GOMEZ CARPIO ALBERTO SAMUEL_5.docx
│   │   │       ├── Certificado_GOMEZ CARPIO ALBERTO SAMUEL_6.docx
│   │   │       ├── Certificado_GOMEZ CARPIO ALBERTO SAMUEL_7.docx
│   │   │       ├── Certificado_GOMEZ CARPIO ALBERTO SAMUEL_8.docx
│   │   │       ├── Certificado_GOMEZ CARPIO ALBERTO SAMUEL_9.docx
│   │   │       ├── Certificado_GOMEZ TICONA NAHUM JOEL.docx
│   │   │       ├── Certificado_GONZALES PONCE LIZETH.docx
│   │   │       ├── Certificado_GONZALES PONCE LIZETH_1.docx
│   │   │       ├── Certificado_GONZALES PONCE LIZETH_2.docx
│   │   │       ├── Certificado_GONZALES PONCE LIZETH_3.docx
│   │   │       ├── Certificado_GONZALES PONCE LIZETH_4.docx
│   │   │       ├── Certificado_GONZALES PONCE LIZETH_5.docx
│   │   │       ├── Certificado_GONZALES PONCE LIZETH_6.docx
│   │   │       ├── Certificado_GONZALES PONCE LIZETH_7.docx
│   │   │       ├── Certificado_GRANADOS SILVESTRE RICHARD JENRY.docx
│   │   │       ├── Certificado_GRANADOS SILVESTRE RICHARD JENRY_1.docx
│   │   │       ├── Certificado_GRANADOS SILVESTRE RICHARD JENRY_2.docx
│   │   │       ├── Certificado_GRANADOS SILVESTRE RICHARD JENRY_3.docx
│   │   │       ├── Certificado_GRANADOS SILVESTRE RICHARD JENRY_4.docx
│   │   │       ├── Certificado_GRANADOS SILVESTRE RICHARD JENRY_5.docx
│   │   │       ├── Certificado_GRANADOS SILVESTRE RICHARD JENRY_6.docx
│   │   │       ├── Certificado_GRANADOS SILVESTRE RICHARD JENRY_7.docx
│   │   │       ├── Certificado_GRANADOS SILVESTRE RICHARD JENRY_8.docx
│   │   │       ├── Certificado_GUERRERO SILVERA RICARDO ENRIQUE.docx
│   │   │       ├── Certificado_GUERRERO SILVERA RICARDO ENRIQUE_1.docx
│   │   │       ├── Certificado_GUERRERO SILVERA RICARDO ENRIQUE_2.docx
│   │   │       ├── Certificado_GUERRERO SILVERA RICARDO ENRIQUE_3.docx
│   │   │       ├── Certificado_GUERRERO SILVERA RICARDO ENRIQUE_4.docx
│   │   │       ├── Certificado_GUERRERO SILVERA RICARDO ENRIQUE_5.docx
│   │   │       ├── Certificado_GUERRERO SILVERA RICARDO ENRIQUE_6.docx
│   │   │       ├── Certificado_GUZMAN ALARCON JUAN GUSTAVO.docx
│   │   │       ├── Certificado_GUZMAN ALARCON JUAN GUSTAVO_1.docx
│   │   │       ├── Certificado_GUZMAN ALARCON JUAN GUSTAVO_2.docx
│   │   │       ├── Certificado_GUZMAN CHUQUICUZMA JAVIER ANTONIO.docx
│   │   │       ├── Certificado_GUZMAN CHUQUICUZMA JAVIER ANTONIO_1.docx
│   │   │       ├── Certificado_GUZMAN CHUQUICUZMA JAVIER ANTONIO_2.docx
│   │   │       ├── Certificado_HELACONDE HUAMANI JOSE ALBERTO.docx
│   │   │       ├── Certificado_HERRERA RODRÍGUEZ HERMES FLAVIO.docx
│   │   │       ├── Certificado_HITO CORDOVA DIEGO HERNANDO.docx
│   │   │       ├── Certificado_HITO CORDOVA DIEGO HERNANDO_1.docx
│   │   │       ├── Certificado_HUAMANI RAMOS ANGEL.docx
│   │   │       ├── Certificado_HUAYNATES SOLORZANO NILTON RUBEN.docx
│   │   │       ├── Certificado_HUERTAS BOLO ANGEL AUGUSTO.docx
│   │   │       ├── Certificado_HUERTAS BOLO ANGEL AUGUSTO_1.docx
│   │   │       ├── Certificado_HURTADO BULNES EDGARD ENRRIQUE.docx
│   │   │       ├── Certificado_ICAHUATE DO SANTOS OSCAR GABEL.docx
│   │   │       ├── Certificado_ICAHUATE DO SANTOS OSCAR GABEL_1.docx
│   │   │       ├── Certificado_ICAHUATE DO SANTOS OSCAR GABEL_2.docx
│   │   │       ├── Certificado_ICAHUATE DO SANTOS OSCAR GABEL_3.docx
│   │   │       ├── Certificado_ICAHUATE DO SANTOS OSCAR GABEL_4.docx
│   │   │       ├── Certificado_ICAHUATE DO SANTOS OSCAR GABEL_5.docx
│   │   │       ├── Certificado_IDME MEDINA JIMMY LEONARDO.docx
│   │   │       ├── Certificado_IDME MEDINA JIMMY LEONARDO_1.docx
│   │   │       ├── Certificado_IDME MEDINA JIMMY LEONARDO_2.docx
│   │   │       ├── Certificado_IDME MEDINA JIMMY LEONARDO_3.docx
│   │   │       ├── Certificado_INGA HUERTA ANGEL ERICSON.docx
│   │   │       ├── Certificado_INGA HUERTA ANGEL ERICSON_1.docx
│   │   │       ├── Certificado_JARA CAMPOS JUAN JAVIER.docx
│   │   │       ├── Certificado_JUAREZ SALAS DEYBIS ANDERSON.docx
│   │   │       ├── Certificado_JUAREZ SALAS DEYBIS ANDERSON_1.docx
│   │   │       ├── Certificado_LAUREL CHUSPI WILFREDO.docx
│   │   │       ├── Certificado_LAUREL CHUSPI WILFREDO_1.docx
│   │   │       ├── Certificado_LAUREL CHUSPI WILFREDO_10.docx
│   │   │       ├── Certificado_LAUREL CHUSPI WILFREDO_11.docx
│   │   │       ├── Certificado_LAUREL CHUSPI WILFREDO_12.docx
│   │   │       ├── Certificado_LAUREL CHUSPI WILFREDO_13.docx
│   │   │       ├── Certificado_LAUREL CHUSPI WILFREDO_14.docx
│   │   │       ├── Certificado_LAUREL CHUSPI WILFREDO_15.docx
│   │   │       ├── Certificado_LAUREL CHUSPI WILFREDO_16.docx
│   │   │       ├── Certificado_LAUREL CHUSPI WILFREDO_2.docx
│   │   │       ├── Certificado_LAUREL CHUSPI WILFREDO_3.docx
│   │   │       ├── Certificado_LAUREL CHUSPI WILFREDO_4.docx
│   │   │       ├── Certificado_LAUREL CHUSPI WILFREDO_5.docx
│   │   │       ├── Certificado_LAUREL CHUSPI WILFREDO_6.docx
│   │   │       ├── Certificado_LAUREL CHUSPI WILFREDO_7.docx
│   │   │       ├── Certificado_LAUREL CHUSPI WILFREDO_8.docx
│   │   │       ├── Certificado_LAUREL CHUSPI WILFREDO_9.docx
│   │   │       ├── Certificado_LAZO ZEBALLOS JAVIER RAMIRO.docx
│   │   │       ├── Certificado_LAZO ZEBALLOS JAVIER RAMIRO_1.docx
│   │   │       ├── Certificado_LAZO ZEBALLOS JAVIER RAMIRO_2.docx
│   │   │       ├── Certificado_LAZO ZEBALLOS JAVIER RAMIRO_3.docx
│   │   │       ├── Certificado_LAZO ZEBALLOS JAVIER RAMIRO_4.docx
│   │   │       ├── Certificado_LAZO ZEBALLOS JAVIER RAMIRO_5.docx
│   │   │       ├── Certificado_LAZO ZEBALLOS JAVIER RAMIRO_6.docx
│   │   │       ├── Certificado_LAZO ZEBALLOS JAVIER RAMIRO_7.docx
│   │   │       ├── Certificado_LAZO ZEBALLOS JAVIER RAMIRO_8.docx
│   │   │       ├── Certificado_LEANO VERA DAVID MOISES.docx
│   │   │       ├── Certificado_LEANO VERA DAVID MOISES_1.docx
│   │   │       ├── Certificado_LEON NIEVES PABLO HERNAN.docx
│   │   │       ├── Certificado_LEON NIEVES PABLO HERNAN_1.docx
│   │   │       ├── Certificado_LEON NIEVES PABLO HERNAN_2.docx
│   │   │       ├── Certificado_LEON NIEVES PABLO HERNAN_3.docx
│   │   │       ├── Certificado_LEON NIEVES PABLO HERNAN_4.docx
│   │   │       ├── Certificado_LEON NIEVES PABLO HERNAN_5.docx
│   │   │       ├── Certificado_LEON NIEVES PABLO HERNAN_6.docx
│   │   │       ├── Certificado_LEON NIEVES PABLO HERNAN_7.docx
│   │   │       ├── Certificado_LESCANO PACHAS FELIX ALEJANDRO.docx
│   │   │       ├── Certificado_LESCANO PACHAS FELIX ALEJANDRO_1.docx
│   │   │       ├── Certificado_LESCANO PACHAS FELIX ALEJANDRO_2.docx
│   │   │       ├── Certificado_LESCANO PACHAS FELIX ALEJANDRO_3.docx
│   │   │       ├── Certificado_LESCANO PACHAS FELIX ALEJANDRO_4.docx
│   │   │       ├── Certificado_LESCANO PAREDES CARLOS ALBERTO.docx
│   │   │       ├── Certificado_LIMA LLERENA CESAR MARTIN.docx
│   │   │       ├── Certificado_LIMA LLERENA CESAR MARTIN_1.docx
│   │   │       ├── Certificado_LIMA LLERENA CESAR MARTIN_10.docx
│   │   │       ├── Certificado_LIMA LLERENA CESAR MARTIN_11.docx
│   │   │       ├── Certificado_LIMA LLERENA CESAR MARTIN_12.docx
│   │   │       ├── Certificado_LIMA LLERENA CESAR MARTIN_13.docx
│   │   │       ├── Certificado_LIMA LLERENA CESAR MARTIN_2.docx
│   │   │       ├── Certificado_LIMA LLERENA CESAR MARTIN_3.docx
│   │   │       ├── Certificado_LIMA LLERENA CESAR MARTIN_4.docx
│   │   │       ├── Certificado_LIMA LLERENA CESAR MARTIN_5.docx
│   │   │       ├── Certificado_LIMA LLERENA CESAR MARTIN_6.docx
│   │   │       ├── Certificado_LIMA LLERENA CESAR MARTIN_7.docx
│   │   │       ├── Certificado_LIMA LLERENA CESAR MARTIN_8.docx
│   │   │       ├── Certificado_LIMA LLERENA CESAR MARTIN_9.docx
│   │   │       ├── Certificado_LINARES AGUIRRE MILCIADES ROMULO.docx
│   │   │       ├── Certificado_LINARES AGUIRRE MILCIADES ROMULO_1.docx
│   │   │       ├── Certificado_LINARES AGUIRRE MILCIADES ROMULO_2.docx
│   │   │       ├── Certificado_LLANOS RIVAS JOSE LUIS.docx
│   │   │       ├── Certificado_LLERENA CHACON CARLOS CESAR.docx
│   │   │       ├── Certificado_LLERENA CHACON CARLOS CESAR_1.docx
│   │   │       ├── Certificado_LOPEZ ENRIQUEZ ERNESTO JOHAN.docx
│   │   │       ├── Certificado_LOPEZ PINTO ROLANDO CHRISTIAN.docx
│   │   │       ├── Certificado_LOPEZ PINTO ROLANDO CHRISTIAN_1.docx
│   │   │       ├── Certificado_LOPEZ PINTO ROLANDO CHRISTIAN_2.docx
│   │   │       ├── Certificado_LOPEZ SALCEDO OMAR IVAN.docx
│   │   │       ├── Certificado_LOZA BANEGAS DERLY.docx
│   │   │       ├── Certificado_LOZA BANEGAS DERLY_1.docx
│   │   │       ├── Certificado_LOZA BANEGAS DERLY_10.docx
│   │   │       ├── Certificado_LOZA BANEGAS DERLY_11.docx
│   │   │       ├── Certificado_LOZA BANEGAS DERLY_12.docx
│   │   │       ├── Certificado_LOZA BANEGAS DERLY_13.docx
│   │   │       ├── Certificado_LOZA BANEGAS DERLY_14.docx
│   │   │       ├── Certificado_LOZA BANEGAS DERLY_2.docx
│   │   │       ├── Certificado_LOZA BANEGAS DERLY_3.docx
│   │   │       ├── Certificado_LOZA BANEGAS DERLY_4.docx
│   │   │       ├── Certificado_LOZA BANEGAS DERLY_5.docx
│   │   │       ├── Certificado_LOZA BANEGAS DERLY_6.docx
│   │   │       ├── Certificado_LOZA BANEGAS DERLY_7.docx
│   │   │       ├── Certificado_LOZA BANEGAS DERLY_8.docx
│   │   │       ├── Certificado_LOZA BANEGAS DERLY_9.docx
│   │   │       ├── Certificado_MAMANI MAMANI LUIS ARMANDO.docx
│   │   │       ├── Certificado_MAMANI MAMANI LUIS ARMANDO_1.docx
│   │   │       ├── Certificado_MAMANI MAMANI LUIS ARMANDO_10.docx
│   │   │       ├── Certificado_MAMANI MAMANI LUIS ARMANDO_11.docx
│   │   │       ├── Certificado_MAMANI MAMANI LUIS ARMANDO_12.docx
│   │   │       ├── Certificado_MAMANI MAMANI LUIS ARMANDO_13.docx
│   │   │       ├── Certificado_MAMANI MAMANI LUIS ARMANDO_14.docx
│   │   │       ├── Certificado_MAMANI MAMANI LUIS ARMANDO_15.docx
│   │   │       ├── Certificado_MAMANI MAMANI LUIS ARMANDO_2.docx
│   │   │       ├── Certificado_MAMANI MAMANI LUIS ARMANDO_3.docx
│   │   │       ├── Certificado_MAMANI MAMANI LUIS ARMANDO_4.docx
│   │   │       ├── Certificado_MAMANI MAMANI LUIS ARMANDO_5.docx
│   │   │       ├── Certificado_MAMANI MAMANI LUIS ARMANDO_6.docx
│   │   │       ├── Certificado_MAMANI MAMANI LUIS ARMANDO_7.docx
│   │   │       ├── Certificado_MAMANI MAMANI LUIS ARMANDO_8.docx
│   │   │       ├── Certificado_MAMANI MAMANI LUIS ARMANDO_9.docx
│   │   │       ├── Certificado_MAMANI MAQUERA JORGE HERNAN.docx
│   │   │       ├── Certificado_MAMANI MAQUERA JORGE HERNAN_1.docx
│   │   │       ├── Certificado_MAMANI MATOS MELENY.docx
│   │   │       ├── Certificado_MAMANI MATOS MELENY_1.docx
│   │   │       ├── Certificado_MAMANI TAIPE ANGEL MARIO.docx
│   │   │       ├── Certificado_MAMANI TAIPE ANGEL MARIO_1.docx
│   │   │       ├── Certificado_MAMANI TAIPE ANGEL MARIO_10.docx
│   │   │       ├── Certificado_MAMANI TAIPE ANGEL MARIO_11.docx
│   │   │       ├── Certificado_MAMANI TAIPE ANGEL MARIO_12.docx
│   │   │       ├── Certificado_MAMANI TAIPE ANGEL MARIO_13.docx
│   │   │       ├── Certificado_MAMANI TAIPE ANGEL MARIO_2.docx
│   │   │       ├── Certificado_MAMANI TAIPE ANGEL MARIO_3.docx
│   │   │       ├── Certificado_MAMANI TAIPE ANGEL MARIO_4.docx
│   │   │       ├── Certificado_MAMANI TAIPE ANGEL MARIO_5.docx
│   │   │       ├── Certificado_MAMANI TAIPE ANGEL MARIO_6.docx
│   │   │       ├── Certificado_MAMANI TAIPE ANGEL MARIO_7.docx
│   │   │       ├── Certificado_MAMANI TAIPE ANGEL MARIO_8.docx
│   │   │       ├── Certificado_MAMANI TAIPE ANGEL MARIO_9.docx
│   │   │       ├── Certificado_MARQUEZ CAMARGO TITO HUGO.docx
│   │   │       ├── Certificado_MARTINEZ DIAS ROBERTO ALEX.docx
│   │   │       ├── Certificado_MARTINEZ YGUIA SANTIAGO JESUS.docx
│   │   │       ├── Certificado_MARTINEZ YUPANQUI YEEN LEONARD.docx
│   │   │       ├── Certificado_MAZUELOS MAZUELOS ELAR EDUARDO.docx
│   │   │       ├── Certificado_MAZUELOS MAZUELOS ELAR EDUARDO_1.docx
│   │   │       ├── Certificado_MAZUELOS MAZUELOS ELAR EDUARDO_2.docx
│   │   │       ├── Certificado_MAZUELOS MAZUELOS ELAR EDUARDO_3.docx
│   │   │       ├── Certificado_MAZUELOS MAZUELOS ELAR EDUARDO_4.docx
│   │   │       ├── Certificado_MEDINA ARREDONDO EDISON JUAN.docx
│   │   │       ├── Certificado_MEDINA ARREDONDO EDISON JUAN_1.docx
│   │   │       ├── Certificado_MEDINA ARREDONDO EDISON JUAN_2.docx
│   │   │       ├── Certificado_MEJIA DURAN LUIS BELTRAN.docx
│   │   │       ├── Certificado_MEJIA DURAN LUIS BELTRAN_1.docx
│   │   │       ├── Certificado_MEJIA HIDALGO VICTOR MANUEL.docx
│   │   │       ├── Certificado_MELGAR BARRIGA MAX ROBERTO.docx
│   │   │       ├── Certificado_MELGAR BARRIGA MAX ROBERTO_1.docx
│   │   │       ├── Certificado_MELGAR BARRIGA MAX ROBERTO_10.docx
│   │   │       ├── Certificado_MELGAR BARRIGA MAX ROBERTO_11.docx
│   │   │       ├── Certificado_MELGAR BARRIGA MAX ROBERTO_12.docx
│   │   │       ├── Certificado_MELGAR BARRIGA MAX ROBERTO_13.docx
│   │   │       ├── Certificado_MELGAR BARRIGA MAX ROBERTO_14.docx
│   │   │       ├── Certificado_MELGAR BARRIGA MAX ROBERTO_15.docx
│   │   │       ├── Certificado_MELGAR BARRIGA MAX ROBERTO_16.docx
│   │   │       ├── Certificado_MELGAR BARRIGA MAX ROBERTO_17.docx
│   │   │       ├── Certificado_MELGAR BARRIGA MAX ROBERTO_2.docx
│   │   │       ├── Certificado_MELGAR BARRIGA MAX ROBERTO_3.docx
│   │   │       ├── Certificado_MELGAR BARRIGA MAX ROBERTO_4.docx
│   │   │       ├── Certificado_MELGAR BARRIGA MAX ROBERTO_5.docx
│   │   │       ├── Certificado_MELGAR BARRIGA MAX ROBERTO_6.docx
│   │   │       ├── Certificado_MELGAR BARRIGA MAX ROBERTO_7.docx
│   │   │       ├── Certificado_MELGAR BARRIGA MAX ROBERTO_8.docx
│   │   │       ├── Certificado_MELGAR BARRIGA MAX ROBERTO_9.docx
│   │   │       ├── Certificado_MENDEZ MENDOZA FRANCISCO JAVIER.docx
│   │   │       ├── Certificado_MENDEZ MENDOZA FRANCISCO JAVIER_1.docx
│   │   │       ├── Certificado_MENDEZ MENDOZA FRANCISCO JAVIER_2.docx
│   │   │       ├── Certificado_MENDOZA CALLALLI JULIO CESAR.docx
│   │   │       ├── Certificado_MERINO MORENO RODNEY ALEXANDER.docx
│   │   │       ├── Certificado_MOGROVEJO RAMIREZ LUIS ALBERTO.docx
│   │   │       ├── Certificado_MONTERO CARBAJAL JHON ROLANDO.docx
│   │   │       ├── Certificado_MONTERO CARBAJAL JHON ROLANDO_1.docx
│   │   │       ├── Certificado_MONTERO CARBAJAL JHON ROLANDO_10.docx
│   │   │       ├── Certificado_MONTERO CARBAJAL JHON ROLANDO_11.docx
│   │   │       ├── Certificado_MONTERO CARBAJAL JHON ROLANDO_2.docx
│   │   │       ├── Certificado_MONTERO CARBAJAL JHON ROLANDO_3.docx
│   │   │       ├── Certificado_MONTERO CARBAJAL JHON ROLANDO_4.docx
│   │   │       ├── Certificado_MONTERO CARBAJAL JHON ROLANDO_5.docx
│   │   │       ├── Certificado_MONTERO CARBAJAL JHON ROLANDO_6.docx
│   │   │       ├── Certificado_MONTERO CARBAJAL JHON ROLANDO_7.docx
│   │   │       ├── Certificado_MONTERO CARBAJAL JHON ROLANDO_8.docx
│   │   │       ├── Certificado_MONTERO CARBAJAL JHON ROLANDO_9.docx
│   │   │       ├── Certificado_MOSCOSO ALVAREZ CESAR IGNACIO.docx
│   │   │       ├── Certificado_MOSCOSO VALDEZ CHRISTIAN SANTY.docx
│   │   │       ├── Certificado_MOSCOSO VALDEZ CHRISTIAN SANTY_1.docx
│   │   │       ├── Certificado_MOSCOSO VALDEZ CHRISTIAN SANTY_2.docx
│   │   │       ├── Certificado_MOSCOSO VALDEZ CHRISTIAN SANTY_3.docx
│   │   │       ├── Certificado_NAVARRO MIRANDA OSCAR MARTIN.docx
│   │   │       ├── Certificado_NAVARRO MIRANDA OSCAR MARTIN_1.docx
│   │   │       ├── Certificado_NAVARRO MIRANDA OSCAR MARTIN_2.docx
│   │   │       ├── Certificado_NAVARRO MIRANDA OSCAR MARTIN_3.docx
│   │   │       ├── Certificado_NAVARRO MIRANDA OSCAR MARTIN_4.docx
│   │   │       ├── Certificado_NINA CHAÑI JAVIER FERNANDO.docx
│   │   │       ├── Certificado_NINA CHAÑI JAVIER FERNANDO_1.docx
│   │   │       ├── Certificado_NINA CHAÑI JAVIER FERNANDO_10.docx
│   │   │       ├── Certificado_NINA CHAÑI JAVIER FERNANDO_11.docx
│   │   │       ├── Certificado_NINA CHAÑI JAVIER FERNANDO_12.docx
│   │   │       ├── Certificado_NINA CHAÑI JAVIER FERNANDO_13.docx
│   │   │       ├── Certificado_NINA CHAÑI JAVIER FERNANDO_14.docx
│   │   │       ├── Certificado_NINA CHAÑI JAVIER FERNANDO_15.docx
│   │   │       ├── Certificado_NINA CHAÑI JAVIER FERNANDO_16.docx
│   │   │       ├── Certificado_NINA CHAÑI JAVIER FERNANDO_2.docx
│   │   │       ├── Certificado_NINA CHAÑI JAVIER FERNANDO_3.docx
│   │   │       ├── Certificado_NINA CHAÑI JAVIER FERNANDO_4.docx
│   │   │       ├── Certificado_NINA CHAÑI JAVIER FERNANDO_5.docx
│   │   │       ├── Certificado_NINA CHAÑI JAVIER FERNANDO_6.docx
│   │   │       ├── Certificado_NINA CHAÑI JAVIER FERNANDO_7.docx
│   │   │       ├── Certificado_NINA CHAÑI JAVIER FERNANDO_8.docx
│   │   │       ├── Certificado_NINA CHAÑI JAVIER FERNANDO_9.docx
│   │   │       ├── Certificado_NINASIVINCHA RUIZ WILLIAM CARLOS.docx
│   │   │       ├── Certificado_NINASIVINCHA RUIZ WILLIAM CARLOS_1.docx
│   │   │       ├── Certificado_NINASIVINCHA RUIZ WILLIAM CARLOS_2.docx
│   │   │       ├── Certificado_NINASIVINCHA RUIZ WILLIAM CARLOS_3.docx
│   │   │       ├── Certificado_NINASIVINCHA RUIZ WILLIAM CARLOS_4.docx
│   │   │       ├── Certificado_NINASIVINCHA RUIZ WILLIAM CARLOS_5.docx
│   │   │       ├── Certificado_NINASIVINCHA RUIZ WILLIAM CARLOS_6.docx
│   │   │       ├── Certificado_NINASIVINCHA RUIZ WILLIAM CARLOS_7.docx
│   │   │       ├── Certificado_NINASIVINCHA RUIZ WILLIAM CARLOS_8.docx
│   │   │       ├── Certificado_NIÑO FERNÁNDEZ HERNAN JEAN PAUL.docx
│   │   │       ├── Certificado_NUÑEZ BALDARRAGO HONORATO WILMER.docx
│   │   │       ├── Certificado_NUÑEZ BALDARRAGO HONORATO WILMER_1.docx
│   │   │       ├── Certificado_NUÑEZ CHUMBEZ FROILAN.docx
│   │   │       ├── Certificado_NUÑEZ CHUMBEZ FROILAN_1.docx
│   │   │       ├── Certificado_OLAZAVAL MILLONES AIDA BEATRIZ.docx
│   │   │       ├── Certificado_OLAZAVAL MILLONES AIDA BEATRIZ_1.docx
│   │   │       ├── Certificado_OSCA MAGAÑO RAUL WALTER.docx
│   │   │       ├── Certificado_OSCA MAGAÑO RAUL WALTER_1.docx
│   │   │       ├── Certificado_OSCA MAGAÑO RAUL WALTER_2.docx
│   │   │       ├── Certificado_OSCA MAGAÑO RAUL WALTER_3.docx
│   │   │       ├── Certificado_OSCA MAGAÑO RAUL WALTER_4.docx
│   │   │       ├── Certificado_OSCA MAGAÑO RAUL WALTER_5.docx
│   │   │       ├── Certificado_OSCA MAGAÑO RAUL WALTER_6.docx
│   │   │       ├── Certificado_OSCA MAGAÑO RAUL WALTER_7.docx
│   │   │       ├── Certificado_OSCA MAGAÑO RAUL WALTER_8.docx
│   │   │       ├── Certificado_OXA CATASI ANICETO DANIEL.docx
│   │   │       ├── Certificado_OXA CATASI ANICETO DANIEL_1.docx
│   │   │       ├── Certificado_OXA CATASI ANICETO DANIEL_2.docx
│   │   │       ├── Certificado_PABLO SOBRADO EVARISTO JOSE.docx
│   │   │       ├── Certificado_PABLO SOBRADO EVARISTO JOSE_1.docx
│   │   │       ├── Certificado_PACHO VELASQUEZ PERCY.docx
│   │   │       ├── Certificado_PACHO VELASQUEZ PERCY_1.docx
│   │   │       ├── Certificado_PACHO VELASQUEZ PERCY_10.docx
│   │   │       ├── Certificado_PACHO VELASQUEZ PERCY_11.docx
│   │   │       ├── Certificado_PACHO VELASQUEZ PERCY_12.docx
│   │   │       ├── Certificado_PACHO VELASQUEZ PERCY_13.docx
│   │   │       ├── Certificado_PACHO VELASQUEZ PERCY_14.docx
│   │   │       ├── Certificado_PACHO VELASQUEZ PERCY_15.docx
│   │   │       ├── Certificado_PACHO VELASQUEZ PERCY_16.docx
│   │   │       ├── Certificado_PACHO VELASQUEZ PERCY_2.docx
│   │   │       ├── Certificado_PACHO VELASQUEZ PERCY_3.docx
│   │   │       ├── Certificado_PACHO VELASQUEZ PERCY_4.docx
│   │   │       ├── Certificado_PACHO VELASQUEZ PERCY_5.docx
│   │   │       ├── Certificado_PACHO VELASQUEZ PERCY_6.docx
│   │   │       ├── Certificado_PACHO VELASQUEZ PERCY_7.docx
│   │   │       ├── Certificado_PACHO VELASQUEZ PERCY_8.docx
│   │   │       ├── Certificado_PACHO VELASQUEZ PERCY_9.docx
│   │   │       ├── Certificado_PAICO VARGAS CESAR REYNALDO.docx
│   │   │       ├── Certificado_PAICO VARGAS CESAR REYNALDO_1.docx
│   │   │       ├── Certificado_PAICO VARGAS CESAR REYNALDO_2.docx
│   │   │       ├── Certificado_PAICO VARGAS CESAR REYNALDO_3.docx
│   │   │       ├── Certificado_PAICO VARGAS CESAR REYNALDO_4.docx
│   │   │       ├── Certificado_PAMPA GALLEGOS JACINTO.docx
│   │   │       ├── Certificado_PAMPA GALLEGOS JACINTO_1.docx
│   │   │       ├── Certificado_PAREDES FABIAN FREDDY YOEL.docx
│   │   │       ├── Certificado_PAREDES FABIAN FREDDY YOEL_1.docx
│   │   │       ├── Certificado_PARI FLORES MARCO ANTONIO.docx
│   │   │       ├── Certificado_PARI FLORES MARCO ANTONIO_1.docx
│   │   │       ├── Certificado_PARI FLORES MARCO ANTONIO_2.docx
│   │   │       ├── Certificado_PARI FLORES MARCO ANTONIO_3.docx
│   │   │       ├── Certificado_PARI FLORES MARCO ANTONIO_4.docx
│   │   │       ├── Certificado_PASAPERA PEÑA JOSE ANTONIO.docx
│   │   │       ├── Certificado_PASAPERA PEÑA JOSE ANTONIO_1.docx
│   │   │       ├── Certificado_PELAEZ URBANO CARLOS ARTURO.docx
│   │   │       ├── Certificado_PELAEZ URBANO CARLOS ARTURO_1.docx
│   │   │       ├── Certificado_PEREZ TINOCO JONNY YOEL.docx
│   │   │       ├── Certificado_PINEDO BANCHO TEOFILO.docx
│   │   │       ├── Certificado_PINEDO BANCHO TEOFILO_1.docx
│   │   │       ├── Certificado_PINEDO BANCHO TEOFILO_10.docx
│   │   │       ├── Certificado_PINEDO BANCHO TEOFILO_11.docx
│   │   │       ├── Certificado_PINEDO BANCHO TEOFILO_12.docx
│   │   │       ├── Certificado_PINEDO BANCHO TEOFILO_13.docx
│   │   │       ├── Certificado_PINEDO BANCHO TEOFILO_14.docx
│   │   │       ├── Certificado_PINEDO BANCHO TEOFILO_15.docx
│   │   │       ├── Certificado_PINEDO BANCHO TEOFILO_16.docx
│   │   │       ├── Certificado_PINEDO BANCHO TEOFILO_17.docx
│   │   │       ├── Certificado_PINEDO BANCHO TEOFILO_2.docx
│   │   │       ├── Certificado_PINEDO BANCHO TEOFILO_3.docx
│   │   │       ├── Certificado_PINEDO BANCHO TEOFILO_4.docx
│   │   │       ├── Certificado_PINEDO BANCHO TEOFILO_5.docx
│   │   │       ├── Certificado_PINEDO BANCHO TEOFILO_6.docx
│   │   │       ├── Certificado_PINEDO BANCHO TEOFILO_7.docx
│   │   │       ├── Certificado_PINEDO BANCHO TEOFILO_8.docx
│   │   │       ├── Certificado_PINEDO BANCHO TEOFILO_9.docx
│   │   │       ├── Certificado_PINEDO CARHUAMACA CARLOS.docx
│   │   │       ├── Certificado_QUENAYA VELASQUEZ PERCY.docx
│   │   │       ├── Certificado_QUENAYA VELASQUEZ PERCY_1.docx
│   │   │       ├── Certificado_QUINTO QUISPE ELVIS YOVANI.docx
│   │   │       ├── Certificado_QUINTO QUISPE ELVIS YOVANI_1.docx
│   │   │       ├── Certificado_QUISPE ACHIRCANA HECTOR EDGAR.docx
│   │   │       ├── Certificado_QUISPE ACHIRCANA HECTOR EDGAR_1.docx
│   │   │       ├── Certificado_QUISPE ACHIRCANA HECTOR EDGAR_2.docx
│   │   │       ├── Certificado_QUISPE ACHIRCANA HECTOR EDGAR_3.docx
│   │   │       ├── Certificado_QUISPE ACHIRCANA HECTOR EDGAR_4.docx
│   │   │       ├── Certificado_QUISPE RAMOS ROY FABIAN.docx
│   │   │       ├── Certificado_QUISPE RAMOS ROY FABIAN_1.docx
│   │   │       ├── Certificado_QUISPE SULLCA FREDY DANIEL.docx
│   │   │       ├── Certificado_QUISPE SULLCA FREDY DANIEL_1.docx
│   │   │       ├── Certificado_QUISPE SULLCA FREDY DANIEL_2.docx
│   │   │       ├── Certificado_QUISPE SULLCA FREDY DANIEL_3.docx
│   │   │       ├── Certificado_QUISPE SULLCA FREDY DANIEL_4.docx
│   │   │       ├── Certificado_QUISPE SULLCA FREDY DANIEL_5.docx
│   │   │       ├── Certificado_QUISPE SULLCA FREDY DANIEL_6.docx
│   │   │       ├── Certificado_QUISPE SULLCA FREDY DANIEL_7.docx
│   │   │       ├── Certificado_QUISPE SULLCA FREDY DANIEL_8.docx
│   │   │       ├── Certificado_QUISPE SULLCA FREDY DANIEL_9.docx
│   │   │       ├── Certificado_RAFAELE TRUJILLO GUIDO.docx
│   │   │       ├── Certificado_RAFAELE TRUJILLO GUIDO_1.docx
│   │   │       ├── Certificado_RAFAELE TRUJILLO GUIDO_10.docx
│   │   │       ├── Certificado_RAFAELE TRUJILLO GUIDO_11.docx
│   │   │       ├── Certificado_RAFAELE TRUJILLO GUIDO_12.docx
│   │   │       ├── Certificado_RAFAELE TRUJILLO GUIDO_13.docx
│   │   │       ├── Certificado_RAFAELE TRUJILLO GUIDO_14.docx
│   │   │       ├── Certificado_RAFAELE TRUJILLO GUIDO_2.docx
│   │   │       ├── Certificado_RAFAELE TRUJILLO GUIDO_3.docx
│   │   │       ├── Certificado_RAFAELE TRUJILLO GUIDO_4.docx
│   │   │       ├── Certificado_RAFAELE TRUJILLO GUIDO_5.docx
│   │   │       ├── Certificado_RAFAELE TRUJILLO GUIDO_6.docx
│   │   │       ├── Certificado_RAFAELE TRUJILLO GUIDO_7.docx
│   │   │       ├── Certificado_RAFAELE TRUJILLO GUIDO_8.docx
│   │   │       ├── Certificado_RAFAELE TRUJILLO GUIDO_9.docx
│   │   │       ├── Certificado_RAMIREZ FLORES JUAN ALBERTO.docx
│   │   │       ├── Certificado_RAMIREZ POMARI ROLANDO.docx
│   │   │       ├── Certificado_RAMIREZ POMARI ROLANDO_1.docx
│   │   │       ├── Certificado_RAYO YUCRA PAULINO DEMETRIO.docx
│   │   │       ├── Certificado_RAYO YUCRA PAULINO DEMETRIO_1.docx
│   │   │       ├── Certificado_RAYO YUCRA PAULINO DEMETRIO_2.docx
│   │   │       ├── Certificado_RAYO YUCRA PAULINO DEMETRIO_3.docx
│   │   │       ├── Certificado_RAYO YUCRA PAULINO DEMETRIO_4.docx
│   │   │       ├── Certificado_RAYO YUCRA PAULINO DEMETRIO_5.docx
│   │   │       ├── Certificado_RAYO YUCRA PAULINO DEMETRIO_6.docx
│   │   │       ├── Certificado_REA MEZA CARLOS ALBERTO.docx
│   │   │       ├── Certificado_REA MEZA CARLOS ALBERTO_1.docx
│   │   │       ├── Certificado_REA MEZA CARLOS ALBERTO_2.docx
│   │   │       ├── Certificado_REYES CORTEZ MILTON CESAR.docx
│   │   │       ├── Certificado_REYES CORTEZ MILTON CESAR_1.docx
│   │   │       ├── Certificado_REYES CORTEZ MILTON CESAR_2.docx
│   │   │       ├── Certificado_RICALDI ZEGARRA JHON WILBER.docx
│   │   │       ├── Certificado_RICALDI ZEGARRA JHON WILBER_1.docx
│   │   │       ├── Certificado_RICALDI ZEGARRA JHON WILBER_2.docx
│   │   │       ├── Certificado_ROBLES LOZANO CHARLES JACK.docx
│   │   │       ├── Certificado_RODRIGUEZ ARANA MAX GUILLERMO.docx
│   │   │       ├── Certificado_RODRIGUEZ ARANA MAX GUILLERMO_1.docx
│   │   │       ├── Certificado_RODRIGUEZ ARANA MAX GUILLERMO_2.docx
│   │   │       ├── Certificado_RODRIGUEZ ARANA MAX GUILLERMO_3.docx
│   │   │       ├── Certificado_RODRIGUEZ ARANA MAX GUILLERMO_4.docx
│   │   │       ├── Certificado_RODRIGUEZ ARANA MAX GUILLERMO_5.docx
│   │   │       ├── Certificado_RODRIGUEZ ARANA MAX GUILLERMO_6.docx
│   │   │       ├── Certificado_RODRIGUEZ ARANA MAX GUILLERMO_7.docx
│   │   │       ├── Certificado_RODRIGUEZ ARANA MAX GUILLERMO_8.docx
│   │   │       ├── Certificado_RODRIGUEZ ARANA MAX GUILLERMO_9.docx
│   │   │       ├── Certificado_RODRIGUEZ AVILA ROBERT MICHAEL.docx
│   │   │       ├── Certificado_RODRIGUEZ MONTAÑEZ JUAN CARLOS.docx
│   │   │       ├── Certificado_RODRIGUEZ MONTAÑEZ JUAN CARLOS_1.docx
│   │   │       ├── Certificado_RODRIGUEZ MONTAÑEZ JUAN CARLOS_2.docx
│   │   │       ├── Certificado_RODRIGUEZ MONTAÑEZ JUAN CARLOS_3.docx
│   │   │       ├── Certificado_RODRIGUEZ MONTAÑEZ JUAN CARLOS_4.docx
│   │   │       ├── Certificado_RUIZ LAURA JOHAO HAMILTON.docx
│   │   │       ├── Certificado_RUIZ VICENTE JOSE PEDRO.docx
│   │   │       ├── Certificado_SALAZAR ROMERO HENRY BELTRAN.docx
│   │   │       ├── Certificado_SALAZAR ROMERO HENRY BELTRAN_1.docx
│   │   │       ├── Certificado_SALAZAR ROMERO HENRY BELTRAN_2.docx
│   │   │       ├── Certificado_SALAZAR ROMERO HENRY BELTRAN_3.docx
│   │   │       ├── Certificado_SALAZAR ROMERO HENRY BELTRAN_4.docx
│   │   │       ├── Certificado_SALCEDO LOPEZ VICTOR ANGEL.docx
│   │   │       ├── Certificado_SALCEDO SOTO JOPHAN DERLYS.docx
│   │   │       ├── Certificado_SALCEDO SOTO JOPHAN DERLYS_1.docx
│   │   │       ├── Certificado_SALCEDO SOTO JOPHAN DERLYS_2.docx
│   │   │       ├── Certificado_SALCEDO SOTO JOPHAN DERLYS_3.docx
│   │   │       ├── Certificado_SALCEDO SOTO JOPHAN DERLYS_4.docx
│   │   │       ├── Certificado_SALCEDO SOTO JOPHAN DERLYS_5.docx
│   │   │       ├── Certificado_SALCEDO SOTO JOPHAN DERLYS_6.docx
│   │   │       ├── Certificado_SALINAS ALEGRE ALEX PARODIS.docx
│   │   │       ├── Certificado_SALINAS ALEGRE ALEX PARODIS_1.docx
│   │   │       ├── Certificado_SALINAS ALEGRE ALEX PARODIS_10.docx
│   │   │       ├── Certificado_SALINAS ALEGRE ALEX PARODIS_11.docx
│   │   │       ├── Certificado_SALINAS ALEGRE ALEX PARODIS_12.docx
│   │   │       ├── Certificado_SALINAS ALEGRE ALEX PARODIS_13.docx
│   │   │       ├── Certificado_SALINAS ALEGRE ALEX PARODIS_14.docx
│   │   │       ├── Certificado_SALINAS ALEGRE ALEX PARODIS_15.docx
│   │   │       ├── Certificado_SALINAS ALEGRE ALEX PARODIS_16.docx
│   │   │       ├── Certificado_SALINAS ALEGRE ALEX PARODIS_17.docx
│   │   │       ├── Certificado_SALINAS ALEGRE ALEX PARODIS_18.docx
│   │   │       ├── Certificado_SALINAS ALEGRE ALEX PARODIS_19.docx
│   │   │       ├── Certificado_SALINAS ALEGRE ALEX PARODIS_2.docx
│   │   │       ├── Certificado_SALINAS ALEGRE ALEX PARODIS_20.docx
│   │   │       ├── Certificado_SALINAS ALEGRE ALEX PARODIS_21.docx
│   │   │       ├── Certificado_SALINAS ALEGRE ALEX PARODIS_22.docx
│   │   │       ├── Certificado_SALINAS ALEGRE ALEX PARODIS_3.docx
│   │   │       ├── Certificado_SALINAS ALEGRE ALEX PARODIS_4.docx
│   │   │       ├── Certificado_SALINAS ALEGRE ALEX PARODIS_5.docx
│   │   │       ├── Certificado_SALINAS ALEGRE ALEX PARODIS_6.docx
│   │   │       ├── Certificado_SALINAS ALEGRE ALEX PARODIS_7.docx
│   │   │       ├── Certificado_SALINAS ALEGRE ALEX PARODIS_8.docx
│   │   │       ├── Certificado_SALINAS ALEGRE ALEX PARODIS_9.docx
│   │   │       ├── Certificado_SALINAS SALAS JUAN CARLOS.docx
│   │   │       ├── Certificado_SALINAS SALAS JUAN CARLOS_1.docx
│   │   │       ├── Certificado_SALINAS SALAS JUAN CARLOS_2.docx
│   │   │       ├── Certificado_SALINAS SALAS JUAN CARLOS_3.docx
│   │   │       ├── Certificado_SANCHEZ VALIENTE ALBERT MAX ULISES.docx
│   │   │       ├── Certificado_SANZ CARDENAS MARCO ANTONIO MELO.docx
│   │   │       ├── Certificado_SANZ CARDENAS MARCO ANTONIO MELO_1.docx
│   │   │       ├── Certificado_SANZ CARDENAS MARCO ANTONIO MELO_2.docx
│   │   │       ├── Certificado_SEGUIL VELASQUEZ ROGER PERCY.docx
│   │   │       ├── Certificado_SEGUIL VELASQUEZ ROGER PERCY_1.docx
│   │   │       ├── Certificado_SEGUIL VELASQUEZ ROGER PERCY_2.docx
│   │   │       ├── Certificado_SEGUIL VELASQUEZ ROGER PERCY_3.docx
│   │   │       ├── Certificado_SEGUIL VELASQUEZ ROGER PERCY_4.docx
│   │   │       ├── Certificado_SEGUIL VELASQUEZ ROGER PERCY_5.docx
│   │   │       ├── Certificado_SEGUIL VELASQUEZ ROGER PERCY_6.docx
│   │   │       ├── Certificado_SEGUIL VELASQUEZ ROGER PERCY_7.docx
│   │   │       ├── Certificado_SEGUIL VELASQUEZ ROGER PERCY_8.docx
│   │   │       ├── Certificado_SERRANO SERRANO HECTOR HERNAN.docx
│   │   │       ├── Certificado_SERRANO SERRANO HECTOR HERNAN_1.docx
│   │   │       ├── Certificado_SERRANO SERRANO HECTOR HERNAN_10.docx
│   │   │       ├── Certificado_SERRANO SERRANO HECTOR HERNAN_11.docx
│   │   │       ├── Certificado_SERRANO SERRANO HECTOR HERNAN_12.docx
│   │   │       ├── Certificado_SERRANO SERRANO HECTOR HERNAN_13.docx
│   │   │       ├── Certificado_SERRANO SERRANO HECTOR HERNAN_2.docx
│   │   │       ├── Certificado_SERRANO SERRANO HECTOR HERNAN_3.docx
│   │   │       ├── Certificado_SERRANO SERRANO HECTOR HERNAN_4.docx
│   │   │       ├── Certificado_SERRANO SERRANO HECTOR HERNAN_5.docx
│   │   │       ├── Certificado_SERRANO SERRANO HECTOR HERNAN_6.docx
│   │   │       ├── Certificado_SERRANO SERRANO HECTOR HERNAN_7.docx
│   │   │       ├── Certificado_SERRANO SERRANO HECTOR HERNAN_8.docx
│   │   │       ├── Certificado_SERRANO SERRANO HECTOR HERNAN_9.docx
│   │   │       ├── Certificado_SILVA PAZ MARCO ANTONIO.docx
│   │   │       ├── Certificado_SILVA PAZ MARCO ANTONIO_1.docx
│   │   │       ├── Certificado_SOCOLA EURIBE JUAN ANDRES.docx
│   │   │       ├── Certificado_SOLIS ESTRADA JOSE LUIS.docx
│   │   │       ├── Certificado_SOLIS ESTRADA JOSE LUIS_1.docx
│   │   │       ├── Certificado_SOLIS ESTRADA JOSE LUIS_10.docx
│   │   │       ├── Certificado_SOLIS ESTRADA JOSE LUIS_11.docx
│   │   │       ├── Certificado_SOLIS ESTRADA JOSE LUIS_12.docx
│   │   │       ├── Certificado_SOLIS ESTRADA JOSE LUIS_13.docx
│   │   │       ├── Certificado_SOLIS ESTRADA JOSE LUIS_14.docx
│   │   │       ├── Certificado_SOLIS ESTRADA JOSE LUIS_15.docx
│   │   │       ├── Certificado_SOLIS ESTRADA JOSE LUIS_16.docx
│   │   │       ├── Certificado_SOLIS ESTRADA JOSE LUIS_17.docx
│   │   │       ├── Certificado_SOLIS ESTRADA JOSE LUIS_18.docx
│   │   │       ├── Certificado_SOLIS ESTRADA JOSE LUIS_2.docx
│   │   │       ├── Certificado_SOLIS ESTRADA JOSE LUIS_3.docx
│   │   │       ├── Certificado_SOLIS ESTRADA JOSE LUIS_4.docx
│   │   │       ├── Certificado_SOLIS ESTRADA JOSE LUIS_5.docx
│   │   │       ├── Certificado_SOLIS ESTRADA JOSE LUIS_6.docx
│   │   │       ├── Certificado_SOLIS ESTRADA JOSE LUIS_7.docx
│   │   │       ├── Certificado_SOLIS ESTRADA JOSE LUIS_8.docx
│   │   │       ├── Certificado_SOLIS ESTRADA JOSE LUIS_9.docx
│   │   │       ├── Certificado_SOTO PEÑA MODESTO.docx
│   │   │       ├── Certificado_SOTO PEÑA MODESTO_1.docx
│   │   │       ├── Certificado_SUAREZ RUEDA CHRISTIAN NOEMI.docx
│   │   │       ├── Certificado_SULLON CHAVEZ CARLOS ALBERTO.docx
│   │   │       ├── Certificado_SULLON CHAVEZ CARLOS ALBERTO_1.docx
│   │   │       ├── Certificado_SULLON CHAVEZ CARLOS ALBERTO_2.docx
│   │   │       ├── Certificado_SULLON CHAVEZ CARLOS ALBERTO_3.docx
│   │   │       ├── Certificado_SULLON CHAVEZ CARLOS ALBERTO_4.docx
│   │   │       ├── Certificado_SULLON CHAVEZ CARLOS ALBERTO_5.docx
│   │   │       ├── Certificado_SULLON CHAVEZ CARLOS ALBERTO_6.docx
│   │   │       ├── Certificado_SULLON CHAVEZ CARLOS ALBERTO_7.docx
│   │   │       ├── Certificado_SULLON CHAVEZ CARLOS ALBERTO_8.docx
│   │   │       ├── Certificado_SULLON CHAVEZ CARLOS ALBERTO_9.docx
│   │   │       ├── Certificado_TACZA SANTANA JOHNNY FLORENCIO.docx
│   │   │       ├── Certificado_TARAZONA ZARATE EBER.docx
│   │   │       ├── Certificado_TEJEDA O'BESSO JULIO JEFFREY.docx
│   │   │       ├── Certificado_TELLO DIAZ ALEX JAVIER.docx
│   │   │       ├── Certificado_TELLO DIAZ ALEX JAVIER_1.docx
│   │   │       ├── Certificado_TELLO DIAZ ALEX JAVIER_10.docx
│   │   │       ├── Certificado_TELLO DIAZ ALEX JAVIER_2.docx
│   │   │       ├── Certificado_TELLO DIAZ ALEX JAVIER_3.docx
│   │   │       ├── Certificado_TELLO DIAZ ALEX JAVIER_4.docx
│   │   │       ├── Certificado_TELLO DIAZ ALEX JAVIER_5.docx
│   │   │       ├── Certificado_TELLO DIAZ ALEX JAVIER_6.docx
│   │   │       ├── Certificado_TELLO DIAZ ALEX JAVIER_7.docx
│   │   │       ├── Certificado_TELLO DIAZ ALEX JAVIER_8.docx
│   │   │       ├── Certificado_TELLO DIAZ ALEX JAVIER_9.docx
│   │   │       ├── Certificado_TORRES CHOQUECOTA ROBERTO.docx
│   │   │       ├── Certificado_TORRES CHOQUECOTA ROBERTO_1.docx
│   │   │       ├── Certificado_TORRES CHOQUECOTA ROBERTO_2.docx
│   │   │       ├── Certificado_TORRES DELGADO JOEL AGRIPINO.docx
│   │   │       ├── Certificado_TORRES DELGADO JOEL AGRIPINO_1.docx
│   │   │       ├── Certificado_TORRES DELGADO JOEL AGRIPINO_2.docx
│   │   │       ├── Certificado_TORRES DELGADO JOEL AGRIPINO_3.docx
│   │   │       ├── Certificado_TORRES DELGADO JOEL AGRIPINO_4.docx
│   │   │       ├── Certificado_TORRES DELGADO JOEL AGRIPINO_5.docx
│   │   │       ├── Certificado_TORRES HUAMANI EDUARDO.docx
│   │   │       ├── Certificado_TORRES HUAMANI EDUARDO_1.docx
│   │   │       ├── Certificado_TORRES HUAMANI EDUARDO_2.docx
│   │   │       ├── Certificado_TORRES HUAMANI EDUARDO_3.docx
│   │   │       ├── Certificado_TORRES HUAMANI EDUARDO_4.docx
│   │   │       ├── Certificado_TORRES HUAMANI EDUARDO_5.docx
│   │   │       ├── Certificado_TORRES HUAMANI EDUARDO_6.docx
│   │   │       ├── Certificado_TORRES RAMIREZ OSCAR MANUEL.docx
│   │   │       ├── Certificado_TORRES RAMIREZ OSCAR MANUEL_1.docx
│   │   │       ├── Certificado_TOTORA HUAYTA CIRO HUGO.docx
│   │   │       ├── Certificado_TURIN SEDANO JUAN PERCY.docx
│   │   │       ├── Certificado_TURPO MARRON EFRAIN ALEJANDRO.docx
│   │   │       ├── Certificado_TURPO MARRON EFRAIN ALEJANDRO_1.docx
│   │   │       ├── Certificado_TURPO MARRON EFRAIN ALEJANDRO_2.docx
│   │   │       ├── Certificado_TURPO MARRON EFRAIN ALEJANDRO_3.docx
│   │   │       ├── Certificado_TURPO MARRON EFRAIN ALEJANDRO_4.docx
│   │   │       ├── Certificado_URQUIZO CAMINO ROSARIO LEONOR.docx
│   │   │       ├── Certificado_URQUIZO CAMINO ROSARIO LEONOR_1.docx
│   │   │       ├── Certificado_URQUIZO CAMINO ROSARIO LEONOR_2.docx
│   │   │       ├── Certificado_URQUIZO CAMINO ROSARIO LEONOR_3.docx
│   │   │       ├── Certificado_VALENZUELA ROMERO ANTONIO CELESTINO.docx
│   │   │       ├── Certificado_VALENZUELA ROMERO ANTONIO CELESTINO_1.docx
│   │   │       ├── Certificado_VALENZUELA ROMERO ANTONIO CELESTINO_2.docx
│   │   │       ├── Certificado_VARGAS GARCIA JUAN AUGUSTO.docx
│   │   │       ├── Certificado_VARGAS VELASQUEZ JOSE SANTOS.docx
│   │   │       ├── Certificado_VARILLAS LAUREANO EDILBERTO.docx
│   │   │       ├── Certificado_VARILLAS LAUREANO EDILBERTO_1.docx
│   │   │       ├── Certificado_VARILLAS LAUREANO EDILBERTO_2.docx
│   │   │       ├── Certificado_VARILLAS LAUREANO EDILBERTO_3.docx
│   │   │       ├── Certificado_VARILLAS LAUREANO EDILBERTO_4.docx
│   │   │       ├── Certificado_VARILLAS LAUREANO EDILBERTO_5.docx
│   │   │       ├── Certificado_VELASQUE VALENCIA SANTOS GUILLERMO.docx
│   │   │       ├── Certificado_VENTURA CABALLERO LIZ MICAELA.docx
│   │   │       ├── Certificado_VENTURA CABALLERO LIZ MICAELA_1.docx
│   │   │       ├── Certificado_VIA CARRANZA EDWIN RUBEN.docx
│   │   │       ├── Certificado_VIA CARRANZA EDWIN RUBEN_1.docx
│   │   │       ├── Certificado_VIA CARRANZA EDWIN RUBEN_2.docx
│   │   │       ├── Certificado_VIA CARRANZA EDWIN RUBEN_3.docx
│   │   │       ├── Certificado_VIA CARRANZA EDWIN RUBEN_4.docx
│   │   │       ├── Certificado_VILLA DE LA CRUZ LUIS ALBERTO.docx
│   │   │       ├── Certificado_VILLA DE LA CRUZ LUIS ALBERTO_1.docx
│   │   │       ├── Certificado_VILLA DE LA CRUZ LUIS ALBERTO_2.docx
│   │   │       ├── Certificado_VILLA DE LA CRUZ LUIS ALBERTO_3.docx
│   │   │       ├── Certificado_VILLA DE LA CRUZ LUIS ALBERTO_4.docx
│   │   │       ├── Certificado_VILLA DE LA CRUZ LUIS ALBERTO_5.docx
│   │   │       ├── Certificado_VILLA DE LA CRUZ LUIS ALBERTO_6.docx
│   │   │       ├── Certificado_VILLA DE LA CRUZ LUIS ALBERTO_7.docx
│   │   │       ├── Certificado_VILLALVA CONDORI GERMAN ARTURO.docx
│   │   │       ├── Certificado_VILLALVA CONDORI GERMAN ARTURO_1.docx
│   │   │       ├── Certificado_VILLALVA CONDORI GERMAN ARTURO_2.docx
│   │   │       ├── Certificado_VILLALVA CONDORI GERMAN ARTURO_3.docx
│   │   │       ├── Certificado_VILLALVA CONDORI GERMAN ARTURO_4.docx
│   │   │       ├── Certificado_VILLALVA CONDORI GERMAN ARTURO_5.docx
│   │   │       ├── Certificado_VILLARAN VASQUEZ CARLOS JAVIER.docx
│   │   │       ├── Certificado_VILLARAN VASQUEZ CARLOS JAVIER_1.docx
│   │   │       ├── Certificado_VILLARAN VASQUEZ CARLOS JAVIER_2.docx
│   │   │       ├── Certificado_YARASCA NIEVA AMADOR JULIAN.docx
│   │   │       ├── Certificado_YARASCA NIEVA AMADOR JULIAN_1.docx
│   │   │       └── Certificado_YARASCA NIEVA AMADOR JULIAN_2.docx
│   │   └── certificates_21.11.2025_13.32.56/
│   │       ├── generation_report.json
│   │       ├── pdf/
│   │       │   └── Certificado_GUZMAN CHUQUICUZMA JAVIER ANTONIO.pdf
│   │       └── word/
│   │           └── Certificado_GUZMAN CHUQUICUZMA JAVIER ANTONIO.docx
│   ├── raw/
│   │   ├── .gitkeep
│   │   └── raw.xlsx
│   └── templates/
│       ├── .gitkeep
│       └── CTRA.docx
└── gui/
    ├── main_window.py
    ├── resources/
    │   └── app.ico
    ├── splash_screen.py
    ├── tabs/
    │   ├── tab_certificates.py
    │   └── tab_etl.py
    └── themes/
        ├── theme_dark.json
        ├── theme_light.json
        └── theme_manager.py
```
