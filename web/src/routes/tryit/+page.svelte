<script lang="ts">
	import FileUpload from '../../lib/components/fileUpload.svelte';
	import ImageUpload from '../../lib/components/imageUpload.svelte';
</script>

<div class="flex flex-col gap-8 py-20">
	<div class="flex flex-col gap-3 mb-14 font-serif text-4xl">
		<h2>Leases, Insurance, Credit Reports, or even the Constitution.</h2>
		<h2>We've got you covered.</h2>
	</div>

	<div class="flex md:flex-row flex-col gap-5">
		<ImageUpload />
		<FileUpload />
	</div>
</div>
