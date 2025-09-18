import React, { useState } from "react";

function App() {
const [prob, setProb] = useState(null);

async function predict() {
const resp = await fetch("http://localhost:5000/predict/game", {
method: "POST",
headers: {
"Content-Type": "application/json",
"X-API-Key": process.env.REACT_APP_API_KEY
},
body: JSON.stringify({
rating_diff: 3.2,
rest_diff: 1,
inj_diff: 0,
closing_home_odds: -110
})
});
const data = await resp.json();
setProb(data);
}

return (
<div className="p-8">
<h1 className="text-xl font-bold mb-4">Sports Predictor</h1>
<button
className="bg-blue-500 text-white px-4 py-2 rounded"
onClick={predict}
>
Predict Example Game
</button>
{prob && (
<pre className="mt-4 bg-gray-100 p-4 rounded">{JSON.stringify(prob, null, 2)}</pre>
)}
</div>
);
}

export default App;
