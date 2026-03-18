import {useToast} from "primevue/usetoast";

export function useAppToast() {
  const toast = useToast();

  const successToast = (message) => {
    toast.add({
      severity: 'success',
      summary: 'Success',
      detail: message,
      life: 3000
    });
  };

  const errorToast = (message) => {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: message,
      life: 3000
    });
  };

  return { successToast, errorToast };
}
