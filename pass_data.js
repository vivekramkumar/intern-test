const express = require('express');
const bodyParser = require('body-parser');
const app = express();
app.use(express.json())
app.set("view engine", "ejs");
app.use(express.static("public"));
app.use(bodyParser.urlencoded({ extended: false }))
app.use(bodyParser.json())
let p = require('python-shell');

//const start = Date.now();
app.get('/',function(req,res) {

  res.render("form.ejs");
});

app.post('/similar',async (req,res)=>{
  
  console.log(req.body.text);
  var final=req.body.text;
  var options = {
      args:
      [
        JSON.stringify(final)

      ]
    }
    const start = Date.now();
    p.PythonShell.run('vivek/final_similar.py', options,   async function(err, results)  {
      var jsonData = results;
      var jsonParsed = JSON.parse(jsonData);
      console.log(jsonParsed);
        res.render('similar_index.ejs',{name:jsonParsed});
        const millis = Date.now() - start;
        console.log(`seconds elapsed = ${(millis / 1000)}`);
      
    });
})



  app.post('/classify',async (req,res)=>{
    console.log(req.body.text);
    console.log(req.body.subject);
    var final=req.body.text;
    var options = {
        args:
        [
          JSON.stringify(final)
  
        ]
      }
      const start = Date.now();
      p.PythonShell.run('tharun/output.py', options,   async function(err, results)  {
        var jsonData = results;
        var jsonParsed = JSON.parse(jsonData);
        console.log(jsonParsed);
          res.render('classify_index.ejs',{name:jsonParsed});
          const millis = Date.now() - start;
          console.log(`seconds elapsed = ${(millis / 1000)}`);
        
      });
    })

    app.post('/sentiment',async (req,res)=>{
      console.log(req.body.text);
      var options = {
          args:
          [
            JSON.stringify(req.body.text)
    
          ]
        }
        const start = Date.now();
        p.PythonShell.run('jerrick/outputjer.py', options,   async function(err, results)  {
          var jsonData = results;
          var jsonParsed = JSON.parse(jsonData);
          console.log(jsonParsed);
            res.render('sentiment_index.ejs',{name:jsonParsed});
            const millis = Date.now() - start;
            console.log(`seconds elapsed = ${(millis / 1000)}`);
          
        });
       
    })


var port=3000;
  app.listen(port, () => {
    console.log(`Server running on port${port}`);
    
  });
