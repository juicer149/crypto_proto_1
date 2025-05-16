+------------------------------------------------------+
|                 User (Programmer)                    |
|  (Använder bibliotekets API via importer)            |
+------------------------------------------------------+
                           |
                           v
+------------------------------------------------------+
|        Public API Layer (pipeline_runner.py)         |
|                                                      |
|  - run_pipeline_from_config(config_file, schema_file,|
|                             pipeline_name, text,     |
|                             alphabet_language)       |
|                                                      |
|  - (ev. andra convenience-metoder)                   |
|                                                      |
|  * Samlar all interaktion för konsumenten            |
|  * Gömmer underliggande lager                        |
+------------------------------------------------------+
                           |
                           v
+------------------------------------------------------+
|       Factory & Validation Layer (pipeline_factory)  |
|                                                      |
|  - validate_pipeline_config()                        |
|  - create_pipelines_from_config()                    |
|                                                      |
|  * Bygger pipelines via ENGINE_REGISTRY              |
|  * Validerar konfiguration mot schema                |
|  * Returnerar färdiga CipherPipeline-objekt          |
+------------------------------------------------------+
                           |
                           v
+------------------------------------------------------+
|       Pipeline Execution Layer (cipher_pipeline)     |
|                                                      |
|  - CipherPipeline                                    |
|      * Tar engines och kör text                      |
|      * Ingen konfiguration eller logik om pipelines  |
+------------------------------------------------------+
                           |
                           v
+------------------------------------------------------+
|             Engines Layer (plugboard, rot, etc.)     |
|                                                      |
|  - PlugboardEngine, StaticRot, AlbertiRot, Vigenere  |
|                                                      |
|  * Varje engine implementerar                        |
|    get_substitution_for_position(pos)                |
+------------------------------------------------------+
                           |
                           v
+------------------------------------------------------+
|             Core Utility Layer (tools/*)             |
|                                                      |
|  - Alphabet                                           |
|  - MessageBit                                        |
|  - TextManipulator                                   |
|                                                      |
|  * Abstraktioner för text, alfabet, formattering     |
+------------------------------------------------------+

