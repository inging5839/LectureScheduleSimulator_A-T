``` mermaid

erDiagram
    MOVIE ||--o{ ACTOR : ""
    MOVIE {
        int id NOT NULL PK
        varchar title
        int year
    }
    ACTOR {
        int id NOT NULL PK
        varchar name
    }
```
