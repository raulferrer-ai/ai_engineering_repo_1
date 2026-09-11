class SearchTool:
    def execute(self, args: dict[str, str]) -> str:
        query = args.get("query", "")
        return f"Resultados encontrados para la búsqueda: '{query}'"
