---


---

<blockquote>
<p>Written with <a href="https://stackedit.io/">StackEdit</a>.</p>
</blockquote>
<h1 id="tesseract-ocr-on-aws-lambda">Tesseract OCR on AWS Lambda</h1>
<p>AWS Lambda function to run tesseract OCR</p>
<h2 id="getting-started">Getting Started</h2>
<p>These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.</p>
<p>The idea is to use a docker container to simulate an AWS lambda environment this allows to build binaries against AWS lambda linux env.<br>
In this example I have build <a href="http://www.leptonica.com/">leptonica</a> and <a href="https://github.com/tesseract-ocr/tesseract">Tesseract Open Source OCR Engine</a>.</p>
<p>The whole idea is leveraged from <a href="https://gist.github.com/barbolo/e59aa45ec8e425a26ec4da1086acfbc7">here</a></p>
<h3 id="prerequisites">Prerequisites</h3>
<p>In order to get started you need docker.<br>
This is a very basic lamdba example and was tested on AWS Lambda Python3.6 environment in 11/2018.<br>
AWS deployment will be automated using <a href="https://serverless.com/">serverless framework</a></p>
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
Default region name <span class="token punctuation">[</span>None<span class="token punctuation">]</span>: us-west-2
Default output <span class="token function">format</span> <span class="token punctuation">[</span>None<span class="token punctuation">]</span>: json
</code></pre>
<p>Test aws access to list available s3 buckets</p>
<pre class=" language-bash"><code class="prism  language-bash">aws s3 <span class="token function">ls</span>
</code></pre>
<p>Additional <a href="https://serverless.com/framework/docs/providers/aws/guide/credentials/">documentation</a></p>
<h3 id="tesseract-lamda-layer">Tesseract lamda layer</h3>
<h4 id="build-custom-lamda-layer">Build custom lamda layer</h4>
<p>A previous version of that example packaged all dependencies<br>
into a zip file which made the deployment slow due to the large size.</p>
<p>One solution is using lambda layer to decouple binary dependencies from the actual lambda code. Both component could be defined in one serverless file but to really leverage decoupelling seperation is recommended.</p>
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
<pre class=" language-bash"><code class="prism  language-bash">./build.sh -l eng,por -m fast <span class="token comment"># downloads FAST models for English and Portugese</span>
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
  tesseractPython36: arn:aws:lambda:ap-southeast-2:***************:layer:tesseractPython36:17
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
<h3 id="lambda-deployment">Lambda Deployment</h3>
<p>Switch to the project root directory<br>
#<a href="https://medium.com/@samme/setting-up-python-3-6-aws-lambda-deployment-package-with-numpy-scipy-pillow-and-scikit-image-de488b2afca6">Setting up Python 3.6 AWS Lambda deployment package with numpy, scipy, pillow and scikit-image</a></p>
<p>#create mylambdapackag folder<br>
mkdir mylambdapackage<br>
#start the docker container and share the folder created</p>
<p>#<a href="https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html?source=post_page---------------------------">https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html?source=post_page---------------------------</a><br>
#<a href="https://github.com/docker-library/official-images/blob/master/library/amazonlinux">https://github.com/docker-library/official-images/blob/master/library/amazonlinux</a></p>
<p>docker run -ti -v ~/mylambdapackage:/mylambdapackage amazonlinux:2018.03.0.20190514</p>
<p>#Inside docker container,<br>
yum update -y &amp;&amp; yum install -y gcc48 gcc48-c++ python36 python36-devel atlas-devel atlas-sse3-devel blas-devel lapack-devel zlib-devel libpng-devel libjpeg-turbo-devel zip freetype-devel findutils libtiff libtiff-devel</p>
<p>#go into /mylambdapackage folder<br>
cd /mylambdapackage<br>
#create Python environment in mylambda folder and activate it<br>
python36 -m venv --copies mylambda &amp;&amp; source mylambda/bin/activate</p>
<p>The–copies parameter will “try to use copies rather than symlinks, even when symlinks are the default for the platform”.</p>
<p>pip3 install -U pip<br>
pip3 install --no-binary :all: numpy scipy pillow<br>
pip3 install --no-binary :all: cython<br>
pip3 install --no-binary :all: scikit-image</p>
<p>#specify where the shared libraries will be stored<br>
libdir="$VIRTUAL_ENV/lib/python3.6/site-packages/lib/"<br>
mkdir -p $libdir<br>
#copy the libraries<br>
cp -v /usr/lib64/atlas/<em>.so.3 $libdir<br>
cp -v /usr/lib64/libquadmath.so.0 $libdir<br>
cp -v /usr/lib64/libgfortran.so.3 $libdir<br>
cp -v /usr/lib64/libpng.so.3 $libdir<br>
cp -v /usr/lib64/libjpeg.so.62 $libdir<br>
cp -v /usr/lib64/libtiff.so.5 $libdir<br>
find $VIRTUAL_ENV/lib/python3.6/site-packages/ -name "</em>.so*" | xargs strip -v</p>
<p>#compress site-packages content into mylambda.zip<br>
pushd $VIRTUAL_ENV/lib/python3.6/site-packages/<br>
zip -r -9 /mylambdapackage/mylambda.zip *<br>
popd<br>
#The created zip file should be located in mylambdapackage/mylambda.zip.</p>
<pre><code>
### Test OCR Lambda function

The lambda function is accepting json post request


#### Lambda Test function

Please refer to the test event, as defined in eventdata.json.

## Built With

* [Tesseract Open Source OCR Engine](https://github.com/tesseract-ocr/tesseract)
* [leptonica](http://www.leptonica.com/)
* [Docker](https://www.docker.com/)
* [Serverless](https://serverless.com/)

## Contributing

Please feel free to comment or contribute especially if your integrating with [serverless](https://serverless.com/) or [AWS SAM](https://docs.aws.amazon.com/lambda/latest/dg/deploying-lambda-apps.html)

## Authors

* **Gerd Wittchen** - *Initial work* - [Idea](https://gist.github.com/barbolo/e59aa45ec8e425a26ec4da1086acfbc7)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

</code></pre>

