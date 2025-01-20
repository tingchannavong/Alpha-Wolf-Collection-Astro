import Fuse from 'fuse.js';
import { useState } from 'react';

// Configs fuse.js
// https://fusejs.io/api/options.html
const options = {
	keys: ['frontmatter.title'],
	includeMatches: true,
	minMatchCharLength: 2,
	threshold: 0.5,
};

function Search({ searchList }) {
	// Following code
    const [query, setQuery] = useState('');
    const fuse = new Fuse(searchList, options);

    // Set a limit to the posts: 10
    const posts = fuse
    .search(query)
    .map((result) => result.item)
    .slice(0, 10);

    function handleOnSearch({ target = {} }) {
        const { value } = target;
        setQuery(value);
    }

    return (
		<>
			<label>Search</label>
			<input type="text" value={query} onChange={handleOnSearch} placeholder="Search posts" />
			{query.length > 1 && (
				<p>
					Found {posts.length} {posts.length === 1 ? 'result' : 'results'} for '{query}'
				</p>
			)}
			<ul>
				{posts &&
					posts.map((post) => (
						<li>
							<a href={`/${post.frontmatter.slug}`}>{post.frontmatter.title}</a>
							{post.frontmatter.description}
						</li>
					))}
			</ul>
		</>
	);

}

export default Search;