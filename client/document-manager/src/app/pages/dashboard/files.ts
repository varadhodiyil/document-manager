export type FileResponse = Files[];

export interface Files {
  added_at: string;
  updated_at: string;
  id: number;
  versions: Version[];
  current_version: number;
  file_name: string;
}

export interface Version {
  id: number;
  version_number: number;
  added_at: string;
  updated_at: string;
  file: number;
}
