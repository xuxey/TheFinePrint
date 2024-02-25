<script lang="ts">
	import Icon from '@iconify/svelte';
	import { FileDropzone, ProgressBar } from '@skeletonlabs/skeleton';
	import { ACCESS_CODE, API_URL, POLLING_INTERVAL_MS } from '$lib/constants';
	import { generateRandomString } from '../utils';

	let files: FileList;

	let loading = false;
	let gptOutput = '';

	const sendDocumentRequest = async () => {
		var data = new FormData();
		data.append('file', files[0]);

		const url = generateRandomString(10);
		const response = await fetch(
			`${API_URL}/summarise_pdf?${new URLSearchParams({ url, access_code: ACCESS_CODE })}`,
			{
				method: 'POST',
				body: data
			}
		);
		loading = true;
		setTimeout(createPollRequest(url, ACCESS_CODE), POLLING_INTERVAL_MS);
		console.log('status', response.status);
		console.log('statusText', response.statusText);
	};

	function createPollRequest(url: string, access_code: string) {
		return () =>
			fetch(`${API_URL}/summary?${new URLSearchParams({ url, access_code })}`)
				.then((response) => {
					console.log('poll fetched');
					if (response.status === 200) {
						response.text().then((text) => {
							loading = false;
							gptOutput = text;
						});
					} else if (response.status == 201) {
						console.log(`Request failed, retrying in ${POLLING_INTERVAL_MS}ms:`, response.status);
						setTimeout(createPollRequest(url, access_code), POLLING_INTERVAL_MS);
					} else {
						console.error('Got Status:', response.status);
						// `Failed with status: ${response.status} ${response.statusText}`;
						loading = false;
					}
				})
				.catch((error) => {
					console.error('Error:', error);
				});
	}
</script>

<div class="flex flex-col gap-8 w-full items-center">
	<FileDropzone name="file-upload" bind:files accept="application/pdf">
		<svelte:fragment slot="message">Upload a Document</svelte:fragment>
		<svelte:fragment slot="meta">We currently support PDFs</svelte:fragment>
	</FileDropzone>

	{#if files}
		<p class="font-sans">File selected: {files[0].name}</p>
	{/if}

	<button
		on:click|preventDefault={sendDocumentRequest}
		class="flex flex-row w-fit bg-gradient-to-r max-h-12 from-blue-800 to-purple-800 rounded-xl px-5 py-3 hover:scale-105 duration-200 items-center gap-4"
	>
		<Icon icon="fluent:sparkle-16-filled" class="text-2xl text-white" />
		<span class="text-white font-semibold font-sans">Analyze this Document</span>
	</button>

	{#if loading}
		<ProgressBar value={undefined} min={0} max={100} track="" meter="bg-blue-800 rounded-md" />
	{/if}

	<div
		class="font-sans p-8 rounded-xl bg-purple-300 bg-opacity-20 {gptOutput == ''
			? 'opacity-0'
			: 'opacity-100'} duration-300"
	>
		<h1 class="text-2xl font-serif mb-3">Key Takeaways</h1>
		<p class="min-h-96">
			{gptOutput}
		</p>
	</div>
</div>
