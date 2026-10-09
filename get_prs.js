const https = require('https'); 
https.get('https://api.github.com/repos/Leofit-Solutions-Grupo01/leofit-pedidos-sistema/pulls?state=open', { headers: { 'User-Agent': 'node.js' } }, (res) => { 
  let data = ''; 
  res.on('data', (c) => data += c); 
  res.on('end', () => { 
    const prs = JSON.parse(data); 
    prs.forEach(pr => console.log(`${pr.number}: ${pr.title} (Branch: ${pr.head.ref})`)) 
  }) 
})
