+------------------------------------------------------+
|                 User (Programmer)                    |
|  (Använder bibliotekets API via importer)            |
+------------------------------------------------------+
                           |
                           v
+------------------------------------------------------+
|        Public API Layer (pipeline_runner.py)         |
|                                                      |
|  - run_pipeline(pipeline_spec, text, alphabet)       |
|                                                      |
|  - (Ev. andra helpers som genererar engines          |
|     med rätt verktyg beroende på kontext)            |
|                                                      |
|  * Samlar all interaktion för konsumenten            |
|  * Gömmer underliggande lager och verktyg            |
+------------------------------------------------------+
                           |
                           v
+------------------------------------------------------+
|             Pipeline Layer (cipher_pipeline.py)      |
|                                                      |
|  - CipherPipeline                                    |
|      * Tar engines eller mixins och kör text         |
|      * Binder ihop verktyg och engines i sekvens     |
|                                                      |
|  * Ingen manipulation, endast orkestrering           |
|  * Pipelines är deklarativa                          |
+------------------------------------------------------+
                           |
                           v
+------------------------------------------------------+
|               Engines Layer (rot, alberti, etc.)     |
|                                                      |
|  - StaticRotEngine                                   |
|  - AlbertiEngine                                     |
|  - VigenereEngine                                    |
|                                                      |
|  * Varje engine använder cipher_tools-mixins         |
|    och orchestrerar manipulationer                   |
|                                                      |
|  * Ingen logik för datahantering, endast strategi    |
+------------------------------------------------------+
                           |
                           v
+------------------------------------------------------+
|          Cipher Tools Layer (cipher_tools/*)         |
|                                                      |
|  - RotMixin, KeywordMixin, PlugboardMixin, etc.      |
|                                                      |
|  * Rena manipulationer via __call__                  |
|  * Kombinerbara mixins för engines                   |
|  * Inga beroenden, inga tillstånd utanför sequence   |
+------------------------------------------------------+
                           |
                           v
+------------------------------------------------------+
|        Core Manipulation Layer (sequence_manipulator)|
|                                                      |
|  - SequenceManipulator                               |
|                                                      |
|  * Enda abstraktionen som kan manipulera sekvenser   |
|  * Fail-fast, strikt, domänneutral                   |
|  * All manipulation går via denna                   |
+------------------------------------------------------+

