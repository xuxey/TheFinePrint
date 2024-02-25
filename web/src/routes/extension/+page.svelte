<script lang="ts">
	import FileUpload from '../../lib/components/fileUpload.svelte';
	import ImageUpload from '../../lib/components/imageUpload.svelte';
</script>

<div class="flex flex-col gap-8 py-20">
	<div class="flex flex-col gap-3 mb-14">
		<h2 class="font-serif text-4xl">Two Clicks. That's all you need.</h2>
		<h2 class="text-2xl font-sans mt-4">
			With the <span class="font-cursive text-3xl mx-1">The Fine Print</span>
			extension for Firefox, summarize any legal document on the web.
		</h2>
	</div>
	<span class="flex flex-row justify-between w-full gap-20">
		<img
			src="firefox.svg"
			alt="Firefox logo"
			class="rotate-0 hover:rotate-45 duration-500 h-[50vh]"
		/>
		<div class="flex flex-col gap-10">
			<div class="">
				<h2 class="text-2xl text-blue-700">Step 1: Download the source</h2>
				<p class="text-lg mt-2">
					Because of Firefox policies, we are in a waiting period before we can publish the
					extension on the official marketplace. In the meantime, please download the source code
					directly using the button below!
					<br />
					<a
						href="https://github.com/xuxey/TheFinePrint/raw/main/tfp-firefox.zip"
						class="w-fit mx-auto flex flex-row bg-gradient-to-r max-h-16 from-blue-800 to-purple-800 rounded-xl px-5 py-3 duration-200 items-center gap-4 text-white font-semibold my-4 hover:scale-105"
					>
						Download the Extension
					</a>
					Start by unzipping the .zip file from the download above
				</p>
			</div>
			<div class="">
				<h2 class="text-2xl text-blue-900">Step 2: Install the extension</h2>
				<p class="text-lg mt-2">
					In Firefox, navigate to <u>about:debugging</u>
					<br />
					Click "This Firefox", followed by "Load Temporary Add On..."
					<br />
					Finally, Select the manifest.json file from the unzipped folder
				</p>
			</div>
			<div class="">
				<h2 class="text-2xl text-blue-950">Step 3: Pin the extension to your toolbar!</h2>
				<p class="text-lg mt-2">
					In your Firefox toolbar, select the extension icon and find the fine print.
					<br />
					Right click it, and select "Pin to Toolbar".
				</p>
			</div>
		</div></span
	>
</div>
