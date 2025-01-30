import type { APIRoute } from "astro";

interface GameFrontmatter {
  title: string;
  players: string;
  duration: string;
}

interface GameData {
  frontmatter: GameFrontmatter;
  file: string;
  url: string;
}

export const GET: APIRoute = async () => {
  // Use import.meta.glob() to import all Markdown files
  const allGames = import.meta.glob<{ frontmatter: GameFrontmatter }>("./boardgames/*.md");

  // Extract frontmatter data from each Markdown file
  const gamesData = await Promise.all(
    Object.entries(allGames).map(async ([filePath, resolver]) => {
      const file = await resolver();
      return {
        frontmatter: file.frontmatter,
        file: filePath,
        url: filePath.replace("./boardgames/", "/boardgames/").replace(".md", "/"),
      };
    })
  );

  return new Response(JSON.stringify(gamesData), {
    headers: {
      "Content-Type": "application/json",
    },
  });
};