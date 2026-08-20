# Referencia de diseño y clasificación

## 1. Pregunta única de entrada

Evita rondas sucesivas. Envía una sola propuesta editable:

```text
Te propongo este dashboard personal:
- Rol/scope: <confirmar>
- Alcance: todos mis tickets, incluidos cerrados / solo activos
- Secciones recomendadas: <lista por rol>
- Privacidad: privado
- Estructura fija: gráfica global + todos mis tickets + secciones elegidas

Confírmame el rol y dime qué secciones mantienes, quitas o añades. Después te
mostraré los filtros y recuentos exactos antes de crear nada.
```

No preguntes al usuario por campos JQL. Traduce sus categorías a campos reales
después de inspeccionar Jira.

## 2. Recomendaciones por rol

Son puntos de partida, no políticas ni pruebas de autorización.

| Rol | Secciones recomendadas | No asumir |
| --- | --- | --- |
| Técnico L1 | Break/Fix; Operativa general | RMA, changes o proyectos sin confirmar scope |
| Técnico L2 | Break/Fix; Trabajo planificado/proyectos; Operativa general | RMA: no se recomienda por defecto |
| IT Infrastructure Engineer | Break/Fix; Proyectos/readiness; Operativa general; RMA solo si lo confirma | Asignación o acceso no prueban readiness RMA |
| RMA coordinator/engineer | RMA de vendor; Diagnóstico previo/Break-Fix; Handoffs logísticos; Operativa general | Que todo ticket con “RMA” en el resumen sea un caso de vendor |
| Logistics / Asset Management | Envíos y recepciones; Compras/materiales; Handoffs RMA; Operativa general | Diagnóstico técnico o aprobación del vendor |
| IT Manager / Lead | Incidentes/operación; Proyectos/changes; Decisiones/aprobaciones; Operativa general | Scope de equipo o miembros; debe confirmarse y autorizarse |

Si el rol no encaja, ofrece categorías por naturaleza del trabajo: incidente,
proyecto/change, solicitud administrativa, vendor/handoff y otros.

## 3. Fuente y clasificación

Consulta tickets actuales con campos mínimos: `key`, `summary`, `project`,
`issuetype`, `status`, `assignee`, `reporter`, `labels`, `components`, `parent` y
los campos de ownership realmente disponibles.

Prioridad para construir predicados:

1. proyecto canónico;
2. tipo de incidencia;
3. componente o campo de ownership aprobado;
4. parent/epic;
5. label mantenida de forma consistente;
6. texto del resumen, solo como fallback frágil y declarado.

No uses el proyecto como sinónimo automático de función. Valida con tickets
reales y muestra un ejemplo sanitizado de qué entra y qué queda fuera.

## 4. Plantillas JQL

Sustituye `BASE`, `RMA_PREDICATE` y demás marcadores; nunca los guardes
literalmente.

```jql
-- Base personal
(assignee = currentUser() OR reporter = currentUser())
ORDER BY statusCategory ASC, updated DESC

-- Solo activos, si la persona lo elige
(assignee = currentUser() OR reporter = currentUser())
AND statusCategory != Done
ORDER BY priority DESC, updated DESC

-- RMA real: proyectos de vendor confirmados
(assignee = currentUser() OR reporter = currentUser())
AND project IN (<RMA_PROJECTS>)
ORDER BY statusCategory ASC, updated DESC

-- Break/Fix: ejemplo; valida proyecto y tipo en vivo
(assignee = currentUser() OR reporter = currentUser())
AND project = <OPERATIONS_PROJECT>
AND issuetype = <INCIDENT_TYPE>
ORDER BY statusCategory ASC, updated DESC

-- Catch-all sin duplicados
BASE AND NOT (RMA_PREDICATE OR BREAKFIX_PREDICATE OR OTHER_PREDICATES)
ORDER BY statusCategory ASC, updated DESC
```

Las secciones deben ser mutuamente excluyentes. Aplica prioridad explícita
cuando un ticket pueda coincidir con más de un predicado. `Operativa general`
es el catch-all recomendado; si la persona no lo quiere, avisa que las secciones
ya no cubrirán necesariamente el total.

## 5. Estructura visual mínima

Siempre incluye:

1. `Gráfico de tarta: <Persona> · Todos mis tickets`, usando el filtro base y
   estadística `Estado`.
2. `Todos mis tickets`, con el mismo filtro base.
3. Una tabla por sección aprobada.

Diseño de dos columnas:

- izquierda, arriba: gráfica global;
- derecha, arriba: todos los tickets;
- debajo: secciones equilibradas por tamaño y frecuencia de uso;
- títulos cortos; evita prefijos redundantes cuando Jira permita renombrarlos.

Columnas por defecto: tipo, clave, resumen, prioridad y estado. Añade proyecto a
vistas cross-project; añade assignee solo en vistas de equipo autorizadas. Usa
10 filas visibles para evitar el bloque interminable; Jira mantiene paginación.

## 6. Preflight antes de crear

Presenta una tabla con:

| Vista | Predicado | Recuento | Solapa con |
| --- | --- | ---: | --- |
| Todos | base | n | — |
| Sección A | base + condición | n | ninguna |
| Otros | base - condiciones previas | n | ninguna |

Comprueba duplicados de dashboard y filtros por nombre y owner. Si existe uno,
propón editarlo o crear otro; no elijas ni borres por tu cuenta.

## 7. Verificación obligatoria

Después de guardar:

1. salir de edición y recargar;
2. confirmar que no hay gadgets sin configurar ni errores de filtro;
3. confirmar que la gráfica usa la base y muestra el total correcto;
4. confirmar títulos, columnas, paginación y orden visual;
5. confirmar que los recuentos exhaustivos suman el total sin duplicados;
6. abrir cada filtro guardado y comprobar JQL y privacidad;
7. conservar el dashboard abierto como entregable.

Si compartir fue autorizado, verifica por separado lectores del dashboard y de
cada filtro. Un dashboard visible con filtros privados está roto para terceros.

## 8. Antipatrones que invalidan el resultado

- una única lista larga;
- gráfica basada en un subconjunto;
- usar solo `assignee = currentUser()` y perder solicitudes creadas por la
  persona;
- secciones solapadas o tickets sin catch-all no declarado;
- RMA inferido por el texto del resumen o recomendado por defecto a L2;
- dashboard compartido con filtros privados;
- crear sin preview y aprobación exacta;
- afirmar que persistió sin salir de edición y recargar.
