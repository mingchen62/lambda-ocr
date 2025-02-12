---


---

<blockquote>
<p>Written with <a href="https://stackedit.io/">StackEdit</a>.</p>
</blockquote>
<h1 id="tesseract-ocr-on-aws-lambda">Tesseract OCR on AWS Lambda</h1>
<p>AWS Lambda function to run tesseract OCR</p>
<h2 id="getting-started">Getting Started</h2>
<p>The idea is to use a docker container to simulate an AWS lambda environment this allows to build binaries against AWS lambda linux env.<br>
In this example I have build <a href="http://www.leptonica.com/">leptonica</a> and <a href="https://github.com/tesseract-ocr/tesseract">Tesseract Open Source OCR Engine</a>.</p>
<p>The whole idea is leveraged from <a href="https://gist.github.com/barbolo/e59aa45ec8e425a26ec4da1086acfbc7">here</a><br>
The main components in this project are two lambda layers and one lambda function.</p>
<h3 id="prerequisites">Prerequisites</h3>
<p>In order to get started you need docker.</p>
<p>AWS deployment can be automated using <a href="https://serverless.com/">serverless framework</a>. An alternative is to use <a href="https://docs.aws.amazon.com/serverless-application-model/index.html">AWS SAM</a>.</p>
<h3 id="installing">Installing</h3>
<h4 id="install-node.js-ubuntu">Install Node.js (Ubuntu)</h4>
<p>Add latest release, add this PPA</p>
<pre class=" language-bash"><code class="prism  language-bash">curl -sL https://deb.nodesource.com/setup_10.x <span class="token operator">|</span> <span class="token function">sudo</span> <span class="token function">bash</span> -
</code></pre>
<p>To install the LTS release, use this PPA</p>
<pre class=" language-bash"><code class="prism  language-bash">curl -sL https://deb.nodesource.com/setup_8.x <span class="token operator">|</span> <span class="token function">sudo</span> <span class="token function">bash</span> -
</code></pre>
<p>Install Nodejs and nvm</p>
<pre class=" language-bash"><code class="prism  language-bash"><span class="token function">sudo</span> apt <span class="token function">install</span> nodejs
</code></pre>
<p>Verify installation</p>
<pre class=" language-bash"><code class="prism  language-bash">node -v
<span class="token function">npm</span> -v
</code></pre>
<p>Other OS installation guides can be found <a href="https://nodejs.org/en/download/package-manager/">here</a></p>
<h4 id="install-serverless">Install Serverless</h4>
<pre class=" language-bash"><code class="prism  language-bash"><span class="token comment"># Install serverless globally</span>
<span class="token function">npm</span> <span class="token function">install</span> serverless -g
</code></pre>
<h4 id="clone-repository">Clone Repository</h4>
<p>Clone the repository and follow the install dependencies steps.</p>
<h4 id="install-aws-cli">Install aws-cli</h4>
<h5 id="using-python3-venv">Using Python3 venv</h5>
<p>In the project directory create python3 venv</p>
<pre class=" language-bash"><code class="prism  language-bash"><span class="token comment"># create venv with name tessenv</span>
python3 -m venv tessenv
</code></pre>
<p>activate the virtual env</p>
<pre class=" language-bash"><code class="prism  language-bash"><span class="token function">source</span> ./tessenv/bin/activate
</code></pre>
<p>verify venv is active pip</p>
<pre class=" language-bash"><code class="prism  language-bash"><span class="token function">which</span> pip
<span class="token comment">#result somepath/tessenv/bin/pip </span>
</code></pre>
<p>Install aws-cli</p>
<pre class=" language-bash"><code class="prism  language-bash">pip <span class="token function">install</span> awscli
</code></pre>
<h5 id="generate-aws-access-keys">Generate AWS access keys</h5>
<p>Follow the AWS <a href="https://aws.amazon.com/premiumsupport/knowledge-center/create-access-key/">tutorial</a> to create access keys<br>
for your user.</p>
<h5 id="setup-aws-access-keys">Setup AWS access keys</h5>
<pre class=" language-bash"><code class="prism  language-bash">$ aws configure
AWS Access Key ID <span class="token punctuation">[</span>None<span class="token punctuation">]</span>: AKIAIOSFODNN7EXAMPLE<span class="token punctuation">(</span>sample<span class="token punctuation">)</span>
AWS Secret Access Key <span class="token punctuation">[</span>None<span class="token punctuation">]</span>: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY<span class="token punctuation">(</span>sample<span class="token punctuation">)</span>
Default region name <span class="token punctuation">[</span>None<span class="token punctuation">]</span>: us-east-1
Default output <span class="token function">format</span> <span class="token punctuation">[</span>None<span class="token punctuation">]</span>: json
</code></pre>
<p>Test aws access to list available s3 buckets</p>
<pre class=" language-bash"><code class="prism  language-bash">aws s3 <span class="token function">ls</span>
</code></pre>
<p>Additional <a href="https://serverless.com/framework/docs/providers/aws/guide/credentials/">documentation</a></p>
<h3 id="tesseract-lamda-layer">Tesseract lamda layer</h3>
<h4 id="build-tesseract-lamda-layer">Build Tesseract lamda layer</h4>
<p>One solution is using lambda layer to decouple binary dependencies from the actual lambda code. It is good for code reuse as well as modular deployment.</p>
<p><a href="https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html">AWS Lambda Layer</a></p>
<pre class=" language-bash"><code class="prism  language-bash"><span class="token function">cd</span> tesseract-layer
</code></pre>
<p>Build lambda layer using lambci/lambda docker container.</p>
<pre class=" language-bash"><code class="prism  language-bash">./build.sh
</code></pre>
<p>By default English best (slow) tesseract model will be<br>
bundled into Lambda layer, but you can override it using<br>
<code>-m</code> parameter (for model type) and <code>-l</code> parameter (comma-separated<br>
list of languages), for example:</p>
<pre class=" language-bash"><code class="prism  language-bash">./build.sh -l eng,chi_sim -m fast <span class="token comment"># downloads FAST models for English and Chinese Simplied</span>
</code></pre>
<p>Verify the folder layer has been created and contains the following folders</p>
<pre class=" language-bash"><code class="prism  language-bash">$ <span class="token function">ls</span> layer
bin <span class="token comment">#compiled tesseract binary</span>
data <span class="token comment">#tesseract language package eng</span>
lib <span class="token comment">#compiled lib dependencies</span>
python <span class="token comment">#python dependencies</span>
</code></pre>
<p>Package the lambda layer</p>
<pre class=" language-bash"><code class="prism  language-bash">serverless package
</code></pre>
<p>Verify the tesseract-layer/.serverless directory has been created and contains a 38MB file <code>tesseractPython36.zip</code>.</p>
<h4 id="deploy-lambda-layer">Deploy lambda layer</h4>
<p>Deploy tesseractPython36 layer to AWS (requires AWS-CLI with valid AWS access keys)</p>
<pre class=" language-bash"><code class="prism  language-bash">$ serverless deploy
Serverless: Packaging service<span class="token punctuation">..</span>.
<span class="token punctuation">..</span>.
<span class="token punctuation">..</span>.
<span class="token punctuation">..</span>.
functions:
  None
layers:
  tesseractPython36: arn:aws:lambda:ap-southeast-2:***************:layer:tesseractPython36:17
</code></pre>
<h4 id="update-lambda-function-layer-reference">Update lambda function layer reference</h4>
<p>Every lambda layer deployment will bump up the lambda layer version.<br>
To make sure the lambda function is referencing the correct version update the version part of<br>
returned layer reference. The reference is output of the layer deployment.</p>
<pre class=" language-bash"><code class="prism  language-bash">$ serverless deploy --region us-east-1
<span class="token punctuation">..</span>.
<span class="token punctuation">..</span>.
<span class="token punctuation">..</span>.
layers:
  tesseractPython36: arn:aws:lambda:us-east-1:***************:layer:tesseractPython36:1
</code></pre>
<p>Alternative query the layer version</p>
<pre class=" language-bash"><code class="prism  language-bash">aws lambda get-layer-version --layer-name tesseractPython36 --version-number <span class="token comment">#versionNumber eg. 1</span>
</code></pre>
<p>Find the and update the version number in the <code>serverless.yml</code> file in the root directory</p>
<pre class=" language-yml"><code class="prism  language-yml"><span class="token comment"># serverless.yml</span>
.
.
.
<span class="token key atrule">tesseract-layer</span><span class="token punctuation">:</span>
    <span class="token key atrule">name</span><span class="token punctuation">:</span> tesseractPython36
    <span class="token key atrule">version</span><span class="token punctuation">:</span> <span class="token number">1</span>
.
.
.
</code></pre>
<h3 id="pil-lambda-layer-for-pil">PIL Lambda layer for PIL</h3>
<p>We will build one more lambda layer for PIL, as it is not included in AWS lambda python runtime.</p>
<h4 id="build-pillow-lamda-layer">Build pillow lamda layer</h4>
<p>Switch to the pillow-layer sub directory</p>
<pre class=" language-bash"><code class="prism  language-bash">$  <span class="token function">cd</span>  pillow-layer
$ ./build.sh pillow
</code></pre>
<h4 id="package-and-deploy-pillow-lamda-layer">Package and Deploy pillow lamda layer</h4>
<pre class=" language-bash"><code class="prism  language-bash">$ serverless package
$ serverless deploy
</code></pre>
<p>You can check AWS lambda console to make sure two customer layers are there. (Lambda -&gt; Layer)</p>
<h3 id="test-ocr-lambda-function">Test OCR Lambda function</h3>
<p>Use Lambda console to create and deploy OCR lambda function( lambda_function.py).</p>
<ul>
<li>Add the two customer built layers to the lambda function</li>
</ul>
<p><img src="https://mchen62.s3.amazonaws.com/lambda_layers_demo.png" alt="enter image description here"></p>
<ul>
<li>Define tesseract environment variables:</li>
</ul>
<p><img src="https://mchen62.s3.amazonaws.com/lambda_demo.png" alt="enter image description here"></p>
<ul>
<li>Adjust parameters in basic setting.<br>
Increase timeout value to 30 seconds for a large image;<br>
Increase memory usage to 1 G  for better performance;</li>
</ul>
<p>After deployment,  lambda function is accepting json post request.<br>
To test lambda deployment, run test script in project root dir:</p>
<pre class=" language-bash"><code class="prism  language-bash">aws lambda invoke  --invocation-type RequestResponse  --function-name <span class="token operator">&lt;</span>lambdafunctname<span class="token operator">&gt;</span>  --region us-east-1  --payload file://test.json outfile
</code></pre>
<p>Please refer to the test event, as defined in test.json. It includes a base64 encoded image.</p>
<h2 id="built-with">Built With</h2>
<ul>
<li><a href="https://github.com/tesseract-ocr/tesseract">Tesseract Open Source OCR Engine</a></li>
<li><a href="http://www.leptonica.com/">leptonica</a></li>
<li><a href="https://www.docker.com/">Docker</a></li>
<li><a href="https://serverless.com/">Serverless</a></li>
</ul>
<h2 id="contributing">Contributing</h2>
<p>Please feel free to comment or contribute especially if your integrating with <a href="https://serverless.com/">serverless</a> or <a href="https://docs.aws.amazon.com/lambda/latest/dg/deploying-lambda-apps.html">AWS SAM</a></p>
<h2 id="authors">Authors</h2>
<ul>
<li><strong>Gerd Wittchen</strong> - <em>Initial work</em> - <a href="https://gist.github.com/barbolo/e59aa45ec8e425a26ec4da1086acfbc7">Idea</a></li>
<li>Ming Chen</li>
</ul>
<h2 id="license">License</h2>
<p>This project is licensed under the MIT License - see the <a href="LICENSE.md">LICENSE.md</a> file for details</p>

