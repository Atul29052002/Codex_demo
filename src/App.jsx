const movieRows = [
  {
    title: 'Trending Now',
    shows: ['Stranger Things', 'You', 'Wednesday', 'Lupin', 'Arcane', 'The Witcher'],
  },
  {
    title: 'Top Picks for You',
    shows: ['Peaky Blinders', 'Money Heist', 'Dark', 'Ozark', 'Black Mirror', 'Narcos'],
  },
  {
    title: 'Continue Watching',
    shows: ['The Crown', 'Breaking Bad', 'The Night Agent', 'The Sandman', 'Bodies', 'Cobra Kai'],
  },
];

const showColors = ['#e50914', '#4c1d95', '#0ea5e9', '#f59e0b', '#10b981', '#ec4899'];

function NavBar() {
  return (
    <header className="navbar">
      <h1 className="logo">NETFLIX</h1>
      <nav>
        <ul>
          <li>Home</li>
          <li>TV Shows</li>
          <li>Movies</li>
          <li>My List</li>
        </ul>
      </nav>
      <button className="sign-in">Sign In</button>
    </header>
  );
}

function Hero() {
  return (
    <section className="hero">
      <div className="overlay" />
      <div className="hero-content">
        <p className="badge">New Series</p>
        <h2>Galactic Frontier</h2>
        <p>
          A reluctant pilot joins a rebel crew to expose a hidden empire conspiracy across the stars.
        </p>
        <div className="hero-buttons">
          <button className="play">▶ Play</button>
          <button className="info">More Info</button>
        </div>
      </div>
    </section>
  );
}

function Row({ title, shows }) {
  return (
    <section className="row">
      <h3>{title}</h3>
      <div className="cards">
        {shows.map((show, index) => (
          <article
            className="card"
            key={show}
            style={{
              background: `linear-gradient(140deg, ${showColors[index % showColors.length]}, #111827)`,
            }}
          >
            <p>{show}</p>
          </article>
        ))}
      </div>
    </section>
  );
}

export default function App() {
  return (
    <div className="app">
      <NavBar />
      <Hero />
      <main>
        {movieRows.map((row) => (
          <Row key={row.title} title={row.title} shows={row.shows} />
        ))}
      </main>
    </div>
  );
}
