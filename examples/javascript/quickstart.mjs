// Domain.com.au API quickstart. Node 18+ (built-in fetch), no dependencies.
//   RAPIDAPI_KEY=... node quickstart.mjs "Bondi Beach"

const HOST = 'domain-com-au1.p.rapidapi.com';

async function get(path, params = {}) {
  const url = new URL(`https://${HOST}${path}`);
  for (const [key, value] of Object.entries(params)) {
    if (value != null) url.searchParams.set(key, value);
  }
  const res = await fetch(url, {
    headers: { 'x-rapidapi-host': HOST, 'x-rapidapi-key': process.env.RAPIDAPI_KEY },
  });
  if (!res.ok) throw new Error(`Domain.com.au API ${res.status}: ${await res.text()}`);
  return (await res.json()).data;
}

const place = process.argv[2] ?? 'Bondi Beach';

// Searches take a suburb token such as bondi-beach-nsw-2026; /locations finds it.
const { results: matches } = await get('/locations', { query: place });
const suburb = matches.find((m) => m.type === 'suburb') ?? matches[0];
if (!suburb) throw new Error(`No Domain location matches "${place}"`);

const { total, results } = await get('/search-listings', {
  listing_type: 'sale',
  locations: suburb.location,
  min_bedrooms: 2,
  page_size: 20,
});
console.log(`${suburb.display_name}: ${total} homes for sale`);
for (const home of results.filter((r) => r.result_type === 'listing').slice(0, 10)) {
  // display_price is the advertised text; price_from is the figure behind it, when supplied.
  const figure = home.price.price_from ? `$${home.price.price_from.toLocaleString('en-US')}` : '-';
  console.log(
    `${home.price.display_price.slice(0, 24).padEnd(24)} ${figure.padStart(12)}  ` +
      `${home.bedrooms} bd  ${home.address.display_address}`
  );
}
