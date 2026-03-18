/*import { ref } from 'vue';
import { useAppToast } from '@/use/useToast.js';

export function useFetch() {
  const { errorToast } = useAppToast();
  const fetchComplete = ref(false);

  const fetchData = async (apiFn, errorMessage) => {
    fetchComplete.value = false;
    try {
      const result = await apiFn();
      return result;
    } catch (e) {
      errorToast(errorMessage);
    } finally {
      fetchComplete.value = true;
    }
  };

  return { fetchComplete, fetchData };

}

*/