# FAQ — Agenda de eventos culturales (Madrid)

Preguntas frecuentes sobre el dataset de **actividades culturales y de ocio** publicado en [datos.madrid.es](https://datos.madrid.es).

## ¿Qué contiene este dataset?

Relación de actividades que se celebran en los **próximos 100 días** (o en curso) en centros municipales: bibliotecas, centros culturales, museos, parques, cines de verano, etc.

## ¿Todos los eventos son gratuitos?

No. Cada fila del CSV incluye el campo **GRATUITO**:

- `1` → actividad gratuita
- `0` → puede tener precio o requerir entrada

Consulta también el campo **PRECIO** cuando exista.

## ¿Hay que inscribirse?

Algunas actividades son gratuitas pero **requieren inscripción previa** (itinerarios guiados, talleres con aforo limitado). En el CSV, la descripción o la URL del evento suelen indicarlo.

## ¿Cómo sé dónde se celebra?

En cada evento encontrarás:

- **NOMBRE-INSTALACION** — centro o espacio
- **DISTRITO-INSTALACION** — distrito de Madrid (Chamberí, Retiro, Hortaleza…)
- **FECHA** y **HORA** — cuándo tiene lugar

## ¿Para qué sirve el PDF del dataset?

El PDF **documenta la estructura** del fichero: nombres de columnas, significado de campos y advertencias. No lista eventos concretos; eso está en el CSV.

## ¿Qué tipo de actividades incluye?

Ejemplos habituales: **cine de verano**, **exposiciones**, **itinerarios en El Retiro**, **magia infantil**, **conciertos**, **rutas por Casa de Campo**.

## Fuente oficial

Datos del **Ayuntamiento de Madrid** — portal municipal www.madrid.es.
