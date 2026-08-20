---
name: jira-personal-dashboard
description: Diseña, crea y verifica dashboards personales de Jira con vista global, gráfica y secciones elegidas según el rol. Use when alguien pida un dashboard personal, quiera ordenar sus tickets por áreas como Break/Fix, RMA, proyectos o solicitudes, o tenga una lista única demasiado larga.
---

# Dashboard personal de Jira

Objetivo: entregar una vista personal clara, compacta y verificable; nunca una
única lista larga sin jerarquía.

Lee [REFERENCE.md](REFERENCE.md) antes de proponer filtros o tocar Jira.

## Contrato obligatorio

- Jira y el navegador son read-only hasta que la persona apruebe el diseño
  exacto: nombre, alcance, secciones y privacidad.
- No infieras el rol, el scope de RMA ni la pertenencia a un equipo por el cargo.
- No modifiques tickets. La autorización cubre solo dashboard, filtros y gadgets.
- Los filtros son privados por defecto. Compartir dashboard y compartir filtros
  son acciones distintas y requieren aprobación expresa.
- Usa campos estables de Jira; no clasifiques por palabras del resumen salvo
  fallback explicado y aprobado.

## Flujo

1. **Descubre en vivo** el usuario, sus tickets y cualquier dashboard/filtro
   personal existente. La base recomendada es:
   ```jql
   (assignee = currentUser() OR reporter = currentUser())
   ORDER BY statusCategory ASC, updated DESC
   ```
   Prueba `Request participants` y `watcher` solo si pueden añadir tickets
   reales; deduplica antes de ampliar la base.
2. **Haz una sola consulta compacta**: rol real, alcance (todos o solo activos),
   secciones deseadas y privacidad. Presenta primero la recomendación del rol
   de [REFERENCE.md](REFERENCE.md), permitiendo añadir o quitar secciones.
3. **Previsualiza antes de escribir**: nombre del dashboard, JQL base, predicado
   de cada sección, orden visual y recuentos actuales. Indica qué es confirmado,
   qué es una propuesta y cualquier clasificación por validar.
4. **Pide aprobación exacta** para crear o editar esos filtros y ese dashboard.
   No conviertas una petición general en permiso para compartirlo o alterar
   tickets.
5. **Construye** filtros con nombres únicos `<Persona> · <Sección>` y gadgets:
   gráfica global, todos los tickets y cada sección aprobada.
6. **Organiza** en dos columnas: gráfica global arriba a la izquierda, todos los
   tickets arriba a la derecha y secciones debajo. Máximo 10 resultados visibles
   por gadget, con paginación; columnas compactas y títulos claros.
7. **Verifica tras recargar**: filtros, títulos, columnas, orden, privacidad,
   recuento global y recuentos por sección. Si las secciones son exhaustivas,
   su suma debe coincidir con el total de la gráfica.

## Salida final

Devuelve el enlace, el alcance exacto, las secciones con sus recuentos, el total
de la gráfica, la privacidad y qué se verificó tras recargar. Señala aparte lo
que no se pudo comprobar. No declares éxito si quedó un gadget sin configurar,
un filtro roto, una sección duplicada o una gráfica que no usa la base global.
