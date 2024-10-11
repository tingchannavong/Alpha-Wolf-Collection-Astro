export function handleSelectChange(e) {
    const showValue = e.target.value;
    const url = new URL(window.location.href);
    url.searchParams.set('show', showValue);
    url.searchParams.set('page', '1'); // Reset to page 1 on show change
    window.location.href = url.toString();
}
