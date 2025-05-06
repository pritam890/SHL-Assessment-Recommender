import React, { useState } from 'react';
import axios from 'axios';

function Search() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchResults = async () => {
    if (!query.trim()) return;
    setLoading(true);
    try {
      const response = await axios.post('http://127.0.0.1:4000/query', { query });
      setResults(response.data.results || []);
    } catch (error) {
      console.error("Error fetching results:", error);
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-tr from-blue-100 via-white to-pink-100 p-6 flex justify-center items-center">
      <div className="w-full max-w-5xl backdrop-blur-lg bg-white/70 shadow-2xl rounded-3xl p-8 border border-blue-200">
        <h1 className="text-5xl font-extrabold text-center text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600 mb-10">
          SHL Assessment Finder
        </h1>

        <div className="flex flex-col md:flex-row items-center gap-4 mb-8">
          <input
            type="text"
            placeholder="Enter your query or a job description text..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="flex-grow w-full md:w-auto p-4 rounded-full border-2 border-blue-300 shadow-inner focus:outline-none focus:ring-2 focus:ring-purple-400 transition"
          />
          <button
            onClick={fetchResults}
            className="bg-gradient-to-r from-blue-500 to-purple-500 text-white px-6 py-3 rounded-full font-semibold hover:scale-105 hover:from-purple-500 hover:to-blue-500 transition-all shadow-lg"
          >
            Search
          </button>
        </div>

        {loading && <p className="text-center text-purple-600 text-lg font-medium">Loading...</p>}

        {!loading && results.length === 0 && (
          <p className="text-center text-gray-500 italic">No results found. Try a different query.</p>
        )}

        {results.length > 0 && (
          <div className="overflow-x-auto mt-8">
            <table className="min-w-full table-auto text-left text-gray-800 rounded-xl overflow-hidden">
              <thead className="bg-gradient-to-r from-purple-300 to-blue-300 text-white">
                <tr>
                  <th className="px-6 py-4">📘 Name</th>
                  <th className="px-6 py-4">⏱ Duration</th>
                  <th className="px-6 py-4">🧪 Test Type</th>
                  <th className="px-6 py-4">🌐 Remote Testing Support</th>
                  <th className="px-6 py-4">🔗 Link</th>
                </tr>
              </thead>
              <tbody className="bg-white">
                {results.map((item, index) => (
                  <tr key={index} className="hover:bg-blue-50 transition">
                    <td className="px-6 py-4 font-semibold">{item["Assessment Name"]}</td>
                    <td className="px-6 py-4">{item["Assessment Length"]}</td>
                    <td className="px-6 py-4">{item["Test Type"]}</td>
                    <td className="px-6 py-4">{item["Remote Testing"]}</td>
                    <td className="px-6 py-4">
                      <a
                        href={item["URL"]}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-600 hover:underline font-medium"
                      >
                        View
                      </a>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

export default Search;
